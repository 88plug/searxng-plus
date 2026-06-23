# SPDX-License-Identifier: AGPL-3.0-or-later
"""Proxmox VE Community Scripts engine.

Searches the community-maintained catalogue at community-scripts.org.
Data is fetched from the PocketBase API and cached locally for 12 hours.
"""

import hashlib
import hmac
import json
import os
import pathlib
import re
import secrets
import typing as t
import unicodedata
import zlib
from urllib.parse import urlencode

from httpx import HTTPError, TimeoutException

from searx import logger
from searx.enginelib import EngineCache
from searx.network import get
from searx.result_types import EngineResults

if t.TYPE_CHECKING:
    from searx.search.processors import RequestParams

engine_type = "offline"
categories = ["it"]
disabled = True
paging = False
time_range_support = False

about = {
    "website": "https://community-scripts.org/",
    "wikidata_id": None,
    "official_api_documentation": "https://community-scripts.org/docs/api/readme",
    "use_official_api": True,
    "require_api_key": False,
    "results": "JSON",
}

_API_BASE = "https://db.community-scripts.org/api/collections/script_scripts/records"
_API_PER_PAGE = 500
_MAX_PAGES = 10
_SCRIPT_URL = "https://community-scripts.org/scripts/{slug}"
_CACHE_TTL = 43200
_MAX_RESULTS = 20
_MAX_CACHE_VALUE_LEN = 10240

_logger = logger.getChild("community_scripts_proxmoxve")
_HMAC_SECRET_KEY: bytes | None = None
CACHE: EngineCache


def _slugify(value: str, max_len: int = 64) -> str:
    value = unicodedata.normalize("NFKD", value)
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-")
    return value[:max_len]


def _fetch_scripts() -> list[dict[str, t.Any]]:
    seen: set[str] = set()
    scripts: list[dict[str, t.Any]] = []

    for page_num in range(1, _MAX_PAGES + 1):
        params = urlencode(
            {
                "perPage": _API_PER_PAGE,
                "page": page_num,
                "fields": "name,slug,description",
                "filter": "(is_deleted=false&&is_disabled=false)",
            }
        )
        url = f"{_API_BASE}?{params}"

        try:
            resp = get(url, timeout=30)
            if resp.status_code != 200:
                _logger.warning("Unexpected PocketBase API status: %s", resp.status_code)
                return []
            data = resp.json()
        except (ValueError, HTTPError, TimeoutException) as exc:
            _logger.warning("Failed to fetch community scripts: %s", exc)
            return []

        if not isinstance(data, dict):
            return []

        items = data.get("items")
        if not isinstance(items, list):
            return []

        for item in items:
            if not isinstance(item, dict):
                continue
            name = item.get("name")
            slug = item.get("slug")
            if not isinstance(name, str) or not isinstance(slug, str):
                continue

            slug = _slugify(slug)
            if not name.strip() or not slug:
                continue

            original_slug = slug
            counter = 1
            while slug in seen:
                slug = f"{original_slug}-{counter}"
                counter += 1
            seen.add(slug)

            description = item.get("description")
            description = description[:500] if isinstance(description, str) else ""
            scripts.append({"name": name.strip(), "slug": slug, "description": description})

        total_pages = data.get("totalPages", 1)
        if page_num >= total_pages:
            break

    return scripts


def setup(engine_settings: dict[str, t.Any]) -> bool:
    global CACHE, _HMAC_SECRET_KEY
    CACHE = EngineCache(engine_settings["name"])

    key = engine_settings.get("hmac_secret_key")
    if key:
        _HMAC_SECRET_KEY = key if isinstance(key, bytes) else key.encode("utf-8")
        return True

    key_from_env = os.getenv("PROXMOXVE_CACHE_HMAC_KEY")
    if key_from_env:
        _HMAC_SECRET_KEY = key_from_env.encode("utf-8")
        return True

    key_file = pathlib.Path(__file__).parent / ".hmac_secret"
    if key_file.exists():
        _HMAC_SECRET_KEY = key_file.read_bytes()
        return True

    new_key = secrets.token_bytes(32)
    try:
        key_file.write_bytes(new_key)
    except OSError as exc:
        _logger.error("Failed to write HMAC secret file: %s", exc)
    _HMAC_SECRET_KEY = new_key
    return True


def _serialize_script(script: dict[str, t.Any]) -> bytes:
    payload = json.dumps(script, ensure_ascii=False).encode("utf-8")
    compressed = zlib.compress(payload, level=6)
    if _HMAC_SECRET_KEY:
        mac = hmac.new(_HMAC_SECRET_KEY, compressed, hashlib.sha256).digest()
        return mac + compressed
    return compressed


def _deserialize_script(data: bytes) -> dict[str, t.Any]:
    if _HMAC_SECRET_KEY:
        mac_size = hashlib.sha256().digest_size
        mac, compressed = data[:mac_size], data[mac_size:]
        expected_mac = hmac.new(_HMAC_SECRET_KEY, compressed, hashlib.sha256).digest()
        if not hmac.compare_digest(mac, expected_mac):
            raise ValueError("HMAC verification failed")
    else:
        compressed = data
    return json.loads(zlib.decompress(compressed).decode("utf-8"))


def _cache_scripts(scripts: list[dict[str, t.Any]]) -> None:
    slugs = []
    for script in scripts:
        slug = script.get("slug")
        if not slug:
            continue
        signed_script = _serialize_script(script)
        if len(signed_script) > _MAX_CACHE_VALUE_LEN:
            continue
        CACHE.set(f"script_{slug}", signed_script, expire=_CACHE_TTL)
        slugs.append(slug)
    CACHE.set("script_slugs_list", slugs, expire=_CACHE_TTL)


def init(engine_settings: dict[str, t.Any]) -> bool:  # pylint: disable=unused-argument
    scripts = _fetch_scripts()
    if scripts:
        try:
            _cache_scripts(scripts)
        except (json.JSONDecodeError, zlib.error) as exc:
            _logger.warning("Failed to cache scripts during init: %s", exc)
            return False
    return True


def _score_script(script: dict[str, t.Any], words: list[str]) -> int:
    score = 0
    name_lower = script["name"].lower()
    desc_lower = script["description"].lower()
    for word in words:
        found = False
        if word in name_lower:
            score += 10
            found = True
        if word in desc_lower:
            score += 5
            found = True
        if not found:
            return 0
    return score


def search(query: str, params: "RequestParams") -> EngineResults:  # pylint: disable=unused-argument
    res = EngineResults()
    if not query or not query.strip():
        return res

    scripts: list[dict[str, t.Any]] = []
    slugs_list = CACHE.get("script_slugs_list")
    if isinstance(slugs_list, list) and slugs_list:
        for slug in slugs_list:
            cached_script = CACHE.get(f"script_{slug}")
            if not cached_script:
                continue
            try:
                scripts.append(_deserialize_script(cached_script))
            except (ValueError, zlib.error, json.JSONDecodeError):
                continue

    if not scripts:
        scripts = _fetch_scripts()
        if scripts:
            try:
                _cache_scripts(scripts)
            except (json.JSONDecodeError, zlib.error):
                pass

    if not scripts:
        return res

    words = query.lower().split()
    scored = [(score, script) for script in scripts if (score := _score_script(script, words)) > 0]
    scored.sort(key=lambda item: item[0], reverse=True)

    for _score, script in scored[:_MAX_RESULTS]:
        content = script["description"]
        if len(content) > 300:
            content = content[:300].rsplit(" ", 1)[0] + "..."
        res.add(
            res.types.MainResult(
                url=_SCRIPT_URL.format(slug=script["slug"]),
                title=script["name"],
                content=content,
            )
        )
    return res