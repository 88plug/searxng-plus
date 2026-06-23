# SPDX-License-Identifier: AGPL-3.0-or-later
"""ARD Sounds (ARD Audiothek) search engine."""

import typing as t

from searx.result_types import EngineResults

if t.TYPE_CHECKING:
    from searx.extended_types import SXNG_Response
    from searx.search.processors import OnlineParams

about = {
    "website": "https://www.ardsounds.de/",
    "wikidata_id": None,
    "official_api_documentation": "https://api.ardaudiothek.de/docs",
    "use_official_api": True,
    "require_api_key": False,
    "results": "JSON",
}

categories = ["music"]
paging = True
results_per_page = 10

_GRAPHQL_URL = "https://api.ardaudiothek.de/graphql"
_QUERY = """
query Search($query: String!, $offset: Int!, $limit: Int!) {
  search(query: $query, offset: $offset, limit: $limit) {
    items { nodes { __typename ... on Item { title sharingUrl description } } }
    programSets { nodes { __typename ... on ProgramSet { title sharingUrl description } } }
  }
}
"""


def request(query: str, params: "OnlineParams") -> None:
    offset = (params["pageno"] - 1) * results_per_page
    params["url"] = _GRAPHQL_URL
    params["method"] = "POST"
    params["headers"]["Content-Type"] = "application/json"
    params["json"] = {
        "query": _QUERY,
        "variables": {"query": query, "offset": offset, "limit": results_per_page},
    }


def response(resp: "SXNG_Response") -> EngineResults:
    res = EngineResults()
    data = resp.json()

    if "errors" in data:
        return res

    search_data = data.get("data", {}).get("search", {})
    for section in ("items", "programSets"):
        nodes = search_data.get(section, {}).get("nodes", [])
        for node in nodes:
            if not isinstance(node, dict):
                continue
            url = node.get("sharingUrl")
            title = node.get("title")
            if not url or not title:
                continue
            res.add(
                res.types.MainResult(
                    url=url,
                    title=title,
                    content=node.get("description") or "",
                )
            )
    return res