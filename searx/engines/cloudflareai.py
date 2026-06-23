# SPDX-License-Identifier: AGPL-3.0-or-later
"""Cloudflare AI engine"""

from json import loads
from searx.exceptions import SearxEngineAPIException

about = {
    "website": "https://ai.cloudflare.com",
    "wikidata_id": None,
    "official_api_documentation": "https://developers.cloudflare.com/workers-ai",
    "use_official_api": True,
    "require_api_key": True,
    "results": "JSON",
}

cf_account_id = ""
cf_ai_api = ""
cf_ai_gateway = ""

cf_ai_model = ""
cf_ai_model_display_name = "Cloudflare AI"

cf_ai_model_assistant = "Keep your answers as short and effective as possible."
cf_ai_model_system = "You are a self-aware language model who is honest and direct about any question from the user."


def request(query, params):

    params["query"] = query
    params["method"] = "POST"
    params["headers"]["Authorization"] = f"Bearer {cf_ai_api}"
    params["headers"]["Content-Type"] = "application/json"

    if cf_ai_gateway:
        params["url"] = (
            f"https://gateway.ai.cloudflare.com/v1/{cf_account_id}/{cf_ai_gateway}/workers-ai/{cf_ai_model}"
        )
    else:
        params["url"] = (
            f"https://api.cloudflare.com/client/v4/accounts/{cf_account_id}/ai/run/{cf_ai_model}"
        )

    params["json"] = {
        "messages": [
            {"role": "assistant", "content": cf_ai_model_assistant},
            {"role": "system", "content": cf_ai_model_system},
            {"role": "user", "content": params["query"]},
        ]
    }

    return params


def response(resp):
    results = []
    json = loads(resp.text)

    if not json.get("success", True) and "errors" in json:
        raise SearxEngineAPIException("Cloudflare AI error: " + str(json["errors"]))

    if "error" in json:
        raise SearxEngineAPIException("Cloudflare AI error: " + str(json["error"]))

    result = json.get("result", {})
    content = result.get("response") or result.get("text") or result.get("description")
    if content:
        results.append(
            {
                "content": content,
                "infobox": cf_ai_model_display_name,
            }
        )

    return results
