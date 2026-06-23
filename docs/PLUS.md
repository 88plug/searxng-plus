# SearXNG-Plus

**SearXNG-Plus** is a community-maintained distribution of [SearXNG](https://github.com/searxng/searxng) that ships fixes and features from open upstream issues and pull requests that were rejected, closed without merge, or left unmerged for long periods.

Upstream SearXNG moves carefully and conservatively. SearXNG-Plus exists for operators who want those community contributions **enabled by default** in a maintained container image—without waiting for upstream acceptance.

- **Repository:** [github.com/88plug/searxng-plus](https://github.com/88plug/searxng-plus)
- **Container image:** [`ghcr.io/88plug/searxng-plus:latest`](https://ghcr.io/88plug/searxng-plus)
- **Upstream base:** Tracks SearXNG `master` with plus-specific commits on the `searxng-plus` branch

---

## What is SearXNG-Plus?

SearXNG-Plus is **not a fork with a different product vision**. It is the same privacy-respecting metasearch engine, extended with:

1. **Bug fixes** drawn from the upstream issue graveyard and stalled PRs
2. **New engines and answerers** that upstream has not merged
3. **Operational improvements** (limiter bypass, query syntax, plugin tuning)
4. **A ready-to-run container** published under the 88plug namespace

Each round bundles a fixed number of fixes and features, documented below. Items reference the original [searxng/searxng](https://github.com/searxng/searxng) issue or PR where applicable.

---

## Docker quick start

Pull and run the published image:

```sh
docker run --rm -d \
  -p 8080:8080 \
  -v searxng-plus-config:/etc/searxng \
  -v searxng-plus-data:/var/cache/searxng \
  ghcr.io/88plug/searxng-plus:latest
```

Open [http://localhost:8080](http://localhost:8080).

### Docker Compose (recommended)

From the `container/` directory in this repository:

```sh
cd container
cp .env.example .env   # optional: adjust SEARXNG_PORT, SEARXNG_VERSION
docker compose up -d
```

The compose file uses `ghcr.io/88plug/searxng-plus:latest` by default and includes a Valkey sidecar for caching.

### First-run configuration

On first start, the entrypoint copies `settings.template.yml` to `/etc/searxng/settings.yml` and generates a random `secret_key`. Plus-added engines are **enabled in that template** (see [Defaults enabled policy](#defaults-enabled-policy)).

To persist settings, mount a volume at `/etc/searxng` as shown above.

---

## Release rounds

### Round 1 — 10 bug fixes

Commit [`77f2eb345`](https://github.com/88plug/searxng-plus/commit/77f2eb345) — *searxng-plus: top 10 community fixes from open issues and closed PRs*

| # | Fix | Upstream refs |
|---|-----|---------------|
| 1 | **Limiter startup noise** — use schema defaults when limiter is disabled; eliminates spurious `limiter.toml` warnings | [#6172](https://github.com/searxng/searxng/issues/6172) |
| 2 | **Favicon DB recursion** — break recursive `properties.init()` during SQLite schema creation | [#6216](https://github.com/searxng/searxng/issues/6216), PR [#6216](https://github.com/searxng/searxng/pull/6216) |
| 3 | **DuckDuckGo news VQD cache** — include `iar` category in VQD cache key so news/images/video tokens do not collide | [#6257](https://github.com/searxng/searxng/issues/6257) |
| 4 | **Brave thumbnails** — read `data-src` and skip inline `data:` / relative placeholder URLs | [#5900](https://github.com/searxng/searxng/issues/5900) |
| 5 | **NVD date parsing** — use `datetime.fromisoformat()` for CVE `published` timestamps | [#6098](https://github.com/searxng/searxng/issues/6098) |
| 6 | **Tracker URL deduplication** — apply one tracker-removal rule per query argument; avoid overlapping-rule races | [#6111](https://github.com/searxng/searxng/issues/6111) |
| 7 | **Wayback Machine bang encoding** — path-suffix bangs (e.g. `!wayback`) pass the query unencoded | [#5547](https://github.com/searxng/searxng/issues/5547) |
| 8 | **Yep engine** — mark broken engine `inactive` (upstream API unreliable) | [#6047](https://github.com/searxng/searxng/issues/6047) |
| 9 | **Wikidata engine** — disable broken infobox engine | [#6292](https://github.com/searxng/searxng/issues/6292) |
| 10 | **YaCy images** — add configurable `base_url` for public YaCy peers | [#6051](https://github.com/searxng/searxng/issues/6051), [#5218](https://github.com/searxng/searxng/issues/5218) |

Additional PR sources: [#6224](https://github.com/searxng/searxng/pull/6224), [#6279](https://github.com/searxng/searxng/pull/6279), [#6300](https://github.com/searxng/searxng/pull/6300), [#6209](https://github.com/searxng/searxng/pull/6209).

---

### Round 2 — 10 bug fixes + 10 features

Commit [`5a555a8d7`](https://github.com/88plug/searxng-plus/commit/5a555a8d7) — *searxng-plus: 10 bugs + 10 features (round 2)*

#### Bug fixes

| # | Fix | Upstream refs |
|---|-----|---------------|
| 1 | **Google News snippet vs timestamp** — stop putting publication date into the `content` field | [#6256](https://github.com/searxng/searxng/issues/6256) |
| 2 | **Kagi optional snippet** — guard against `KeyError` on unpromoted results | [#6252](https://github.com/searxng/searxng/issues/6252) |
| 3 | **Google silent empty results** — log a warning when Google returns zero results unexpectedly | [#6171](https://github.com/searxng/searxng/issues/6171) |
| 4 | **`publishedDate` formatting** — handle microseconds and timezone offsets consistently | [#5121](https://github.com/searxng/searxng/issues/5121) |
| 5 | **TrackerPatterns double init** — fix race when tracker DB initializes concurrently | [#5081](https://github.com/searxng/searxng/issues/5081) |
| 6 | **YaCy pagination** — JSON extraction fallback when HTML pagination markers are absent | [#5678](https://github.com/searxng/searxng/issues/5678) |
| 7 | **BCP47 script subtags** — accept locales like `zh-Hans` without `ValidationException` | [#5017](https://github.com/searxng/searxng/issues/5017) |
| 8 | **Cloudflare AI gateway** — support direct API and gateway URL modes | [#5035](https://github.com/searxng/searxng/issues/5035) |
| 9 | **ChinaSo fake URLs** — resolve redirect chains to real destination URLs | [#4694](https://github.com/searxng/searxng/issues/4694) |
| 10 | **Custom locales in settings** — allow operator-defined locale entries in `settings.yml` | [#5996](https://github.com/searxng/searxng/issues/5996) |

#### Features

| # | Feature | Upstream refs |
|---|---------|---------------|
| 1 | **Limiter bypass key** — trusted clients can pass `X-SearXNG-Limiter-Bypass` | [#6227](https://github.com/searxng/searxng/issues/6227) |
| 2 | **ClearURL fetch timeout** — configurable timeout for the ClearURL plugin | [#6043](https://github.com/searxng/searxng/issues/6043) |
| 3 | **Require-all-terms bang** — `!+` prefix requires every query term in results | [#6095](https://github.com/searxng/searxng/issues/6095) |
| 4 | **Proxmox VE community scripts engine** — search community install scripts | [#5746](https://github.com/searxng/searxng/issues/5746) |
| 5 | **Neocities engine** — search neocities.org sites | [#6287](https://github.com/searxng/searxng/issues/6287) |
| 6 | **BASE engine enabled** — Bielefeld Academic Search Engine on by default | [#5283](https://github.com/searxng/searxng/issues/5283) |
| 7 | **Internet Archive Scholar engine** — academic search via scholar.archive.org | [#4038](https://github.com/searxng/searxng/issues/4038) |
| 8 | **Word definition answerer** — `define <word>` instant definitions | [#4111](https://github.com/searxng/searxng/issues/4111) |
| 9 | **cartes.app engine** — map search via cartes.app | [#5938](https://github.com/searxng/searxng/issues/5938) |
| 10 | **ARD Sounds engine** — search ARD audio catalog via GraphQL | [#6094](https://github.com/searxng/searxng/issues/6094) |

#### Infrastructure (Round 2)

- Container branding: `ghcr.io/88plug/searxng-plus`
- GitHub Actions CI workflow (`.github/workflows/88plug-ci.yml`)
- Unit tests for limiter bypass and require-all-terms query parsing

---

### Round 3 — 20 bug fixes + 20 features

Commit *searxng-plus: 20 bugs + 20 features (round 3)* — ports open upstream PRs and fixes graveyard issues.

#### Bug fixes

| # | Fix | Upstream refs |
|---|-----|---------------|
| 1 | **Autocomplete Chromium scores** — attach `google:suggestrelevance` so Chromium shows more than 3 suggestions | PR [#6294](https://github.com/searxng/searxng/pull/6294) |
| 2 | **Google News DOM update** — title/author/metadata xpaths for Google's latest news HTML | PR [#6284](https://github.com/searxng/searxng/pull/6284) |
| 3 | **ChinaSo terminated media** — remove dead images/videos engines; news-only | PR [#6277](https://github.com/searxng/searxng/pull/6277) |
| 4 | **Tracker rule caching** — materialize ClearURL rules once per process, not per URL | PR [#6194](https://github.com/searxng/searxng/pull/6194) |
| 5 | **Known cookies only** — preferences page and clear-cookies respect known preference cookies | PR [#4149](https://github.com/searxng/searxng/pull/4149), [#3763](https://github.com/searxng/searxng/issues/3763) |
| 6 | **Library of Congress 403** — return empty results on access-denied instead of JSON parse crash | [#4810](https://github.com/searxng/searxng/issues/4810) |
| 7 | **PyPI engine parsing** — update xpaths for current warehouse HTML layout | [#4093](https://github.com/searxng/searxng/issues/4093) |
| 8 | **Artic Cloudflare images** — use API thumbnail LQIP as `img_src` when IIIF URLs are blocked | [#5176](https://github.com/searxng/searxng/issues/5176), [#6136](https://github.com/searxng/searxng/issues/6136) |
| 9 | **Startpage autocomplete** — add required headers and handle HTTP 204 empty responses | [#4334](https://github.com/searxng/searxng/issues/4334) |
| 10 | **DuckDuckGo news filtering** — pass `iar=news` and skip non-news results in news category | [#6257](https://github.com/searxng/searxng/issues/6257) |
| 11 | **Brave 429 handling** — raise `SearxEngineTooManyRequestsException` with configured suspend time | [#4653](https://github.com/searxng/searxng/issues/4653) |
| 12 | **Centered answer box** — align `#answers` in centered layout breakpoints | [#4832](https://github.com/searxng/searxng/issues/4832) |
| 13 | **RTL URL spacing** — fix host-only URL separator in RTL result templates | [#3724](https://github.com/searxng/searxng/issues/3724) |
| 14 | **Wikipedia en-SG widgets** — map `en-SG` to English wiki, not territory-derived Chinese | [#3343](https://github.com/searxng/searxng/issues/3343) |
| 15 | **Preferences persistence** — refresh preference cookies on HTML responses with `path=/` | [#2353](https://github.com/searxng/searxng/issues/2353) |
| 16 | **Autocomplete deduplication** — filter empty and duplicate suggestions | [#3337](https://github.com/searxng/searxng/issues/3337) |
| 17 | **RTL bang display** — `unicode-bidi: plaintext` on search input for RTL locales | [#2699](https://github.com/searxng/searxng/issues/2699) |
| 18 | **SSL context documentation** — document httpx SSL context reuse in network client | [#2977](https://github.com/searxng/searxng/issues/2977) |
| 19 | **Tube Archivist API** — trailing slash on `/api/search/?` endpoint (v0.5.9+) | [#5505](https://github.com/searxng/searxng/issues/5505) |
| 20 | **Instance name in theme** — `display_instance_name: true` plus header branding | PR [#4208](https://github.com/searxng/searxng/pull/4208) |

#### Features

| # | Feature | Upstream refs |
|---|---------|---------------|
| 1 | **Icons8 engine** — icon search via icons8.com API | PR [#6123](https://github.com/searxng/searxng/pull/6123) |
| 2 | **Neosearch engine** — general search via neosearch.org | PR [#6274](https://github.com/searxng/searxng/pull/6274) |
| 3 | **Picjumbo engine** — free stock photos | PR [#6273](https://github.com/searxng/searxng/pull/6273) |
| 4 | **Magnific engine** — curated free images | PR [#6272](https://github.com/searxng/searxng/pull/6272) |
| 5 | **StockSnap engine** — CC0 stock photography | PR [#6271](https://github.com/searxng/searxng/pull/6271) |
| 6 | **Shopify stock engine** — Shopify burst gallery images | PR [#6270](https://github.com/searxng/searxng/pull/6270) |
| 7 | **Sina news engine** — Chinese news via json_engine | PR [#6259](https://github.com/searxng/searxng/pull/6259) |
| 8 | **Giphy enabled** — GIF/image search on by default | merged upstream |
| 9 | **Findfiles enabled** — file search (all/images/videos/music) on by default | merged upstream |
| 10 | **Luxxle enabled** — general/images/videos/news on by default | merged upstream |
| 11 | **Searchzee enabled** — web and news search on by default | merged upstream |
| 12 | **Podchaser enabled** — podcast search on by default | merged upstream |
| 13 | **Vuhuv enabled** — general/images/videos on by default | merged upstream |
| 14 | **S1search enabled** — searchtoday and infospace on by default | merged upstream |
| 15 | **Resulthunter enabled** — web and images on by default | merged upstream |
| 16 | **Seekninja enabled** — general search on by default | merged upstream |
| 17 | **Chatnoir enabled** — general search on by default | merged upstream |
| 18 | **Heexy enabled** — general and images on by default | merged upstream |
| 19 | **abcnyheter enabled** — Norwegian news on by default | merged upstream |
| 20 | **Plus documentation site** — `docs/PLUS.md` landing page and updated `README.rst` | 88plug |

---

### Round 4 — Bot bypass: curl_cffi impersonate + Tor profile

*Network-layer evaluation and opt-in bot-bypass tooling (upstream PR [#5476](https://github.com/searxng/searxng/pull/5476) POC port).*

#### Real evaluation (2026-06-22, egress from builder container)

Probed five bot-sensitive engines with five transport modes. **Usable** = HTTP 200 + parseable results + no CAPTCHA/challenge markers.

| Engine | httpx + cipher shuffle | curl_cffi chrome | curl_cffi firefox | Tor + httpx | Tor + chrome |
|--------|------------------------|------------------|-------------------|-------------|--------------|
| Mojeek | yes | yes | yes | timeout | 403 |
| DuckDuckGo HTML | yes | **challenge** | **challenge** | yes | 403 |
| Startpage | no* | no* | no* | no* | no* |
| Brave | 429 CAPTCHA | curl error | curl error | timeout | timeout |
| Qwant | no* | no* | no* | no* | no* |

\*Startpage/Qwant simple probes did not match engine HTML flow; transport alone does not fix token/session engines.

**Conclusions:**

1. **curl_cffi impersonate** helps engines that fingerprint TLS/HTTP stacks (Mojeek POC). It is **not** a global default — DuckDuckGo HTML POST gets `202` + `anomaly-modal` with chrome/firefox impersonation while plain httpx works from the same IP.
2. **Tor outgoing proxy** rotates egress but adds 3–10s latency, times out or 403s many commercial engines, and is useless for operator privacy theater (engines still see *a* IP, just a Tor exit).
3. **Cipher shuffle** (issue [#2977](https://github.com/searxng/searxng/issues/2977)) remains the default httpx mitigation; impersonate is per-engine opt-in.

#### What shipped

| Item | Default | Notes |
|------|---------|-------|
| `httpx_curl_cffi==0.1.5` dependency | installed | Browser TLS+HTTP fingerprint via [curl_cffi](https://github.com/lexiforest/curl_cffi) |
| `network.impersonate` setting | **off** | Per-engine: `chrome`, `firefox`, `safari`, `edge` |
| Mojeek impersonate | opt-in | `network.impersonate: chrome` in settings (engine still `disabled: true` upstream) |
| Tor compose profile | **off** | `docker compose --profile tor up -d` + `container/settings.tor.example.yml` |
| FlareSolverr | not added | Sidecar without network client is useless; CAPTCHA bugs are mostly non-Cloudflare |

#### Enable curl_cffi impersonate (per engine)

```yaml
engines:
  - name: mojeek
    disabled: false
    network:
      impersonate: chrome
```

Child engines can reference a parent network: `network: mojeek`.

**Do not** enable impersonate on DuckDuckGo — live eval showed it triggers DDG's anomaly modal.

#### Enable Tor outgoing proxy

```sh
cd container
docker compose --profile tor up -d
```

Merge `container/settings.tor.example.yml` into `/etc/searxng/settings.yml` (or uncomment the `outgoing.proxies` block in `searx/settings.yml`). Requires `using_tor_proxy: true` and `extra_proxy_timeout: 10` (seconds).

Onion-category engines (Ahmia, etc.) require Tor; the `ahmia_filter` plugin enforces this.

---

## Just-works defaults (round 5)

SearXNG-Plus ships tuned for self-hosters who want results without tuning YAML:

| Setting | Value | Why |
|---------|-------|-----|
| `general.instance_name` | `SearXNG-Plus` | Clear branding |
| `search.autocomplete` | `duckduckgo` | Works without API keys |
| `search.favicon_resolver` | `duckduckgo` | Favicons in results out of the box |
| `server.limiter` | `false` | No spurious `limiter.toml` noise on private instances |
| `server.image_proxy` | `true` | Thumbnails work through the instance |
| Mojeek engines | **enabled** | `curl_cffi` chrome impersonate (live-eval verified) |
| Valkey sidecar | **on** in compose | `SEARXNG_VALKEY_URL` wired automatically |
| Tor / global impersonate | **off** | Opt-in only — eval showed DDG breaks with global impersonate |

Docker Compose brings up core + Valkey. First run copies `settings.template.yml` with all plus engines enabled.

---

## Defaults enabled policy

SearXNG-Plus follows a simple rule:

> **If we add it, we enable it.**

When a feature or engine is introduced in a plus round, it ships **enabled in default settings** unless there is a strong reason not to (broken upstream API, legal concern, or requiring operator secrets).

### What this means in practice

| Category | Policy |
|----------|--------|
| **New engines** | `disabled: false` (or `disabled` key removed) in `searx/settings.yml` |
| **New answerers** | Registered and active without extra configuration |
| **New plugins / server options** | Sensible defaults documented; secrets still required from the operator |
| **Broken upstream engines** | Explicitly `disabled: true` and/or `inactive: true` (e.g. yep, wikidata) |
| **Docker first run** | `container/settings.template.yml` explicitly enables plus-added engines |

### Plus-added engines enabled by default

These engines are enabled on first run (Round 2 defaults, commit [`6331c8b4a`](https://github.com/88plug/searxng-plus/commit/6331c8b4a)):

| Engine | Shortcut | Category |
|--------|----------|----------|
| neocities | `neo` | general |
| cartes | `cart` | map |
| internet archive scholar | `ias` | science |
| ard sounds | `ard` | music |
| base | `bs` | science |
| proxmox ve community scripts | `pve` | it |

### Opting out

Operators can disable any engine in `/etc/searxng/settings.yml`:

```yaml
engines:
  - name: neocities
    disabled: true
```

Or use `use_default_settings.engines.remove` to drop engines from the active set entirely. See the [SearXNG settings documentation](https://docs.searxng.org/admin/settings/index.html).

---

## Relationship to upstream

SearXNG-Plus **tracks upstream SearXNG** and applies plus commits on top. It is intended for self-hosters who want community fixes today.

- Bug reports and feature ideas should reference the original upstream issue when possible
- Plus-specific packaging and release notes live in this repository
- Contributions that meet upstream quality bars should still be proposed to [searxng/searxng](https://github.com/searxng/searxng) directly

---

## Links

- **SearXNG-Plus repository:** https://github.com/88plug/searxng-plus
- **Container image:** https://ghcr.io/88plug/searxng-plus
- **Upstream SearXNG:** https://github.com/searxng/searxng
- **Upstream documentation:** https://docs.searxng.org