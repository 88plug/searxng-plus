# SPDX-License-Identifier: AGPL-3.0-or-later
"""Word definition answerer using DuckDuckGo instant answers API."""

import re
from urllib.parse import urlencode

from flask_babel import gettext

from searx.network import get
from searx.result_types import Answer
from searx.result_types.answer import BaseAnswer

from . import Answerer, AnswererInfo

_WORD_RE = re.compile(r'^[a-zA-Z][a-zA-Z\-\'\.]{0,48}$')


class SXNGAnswerer(Answerer):
    """Literal word definitions at the top of results."""

    keywords = ["define"]

    def info(self) -> AnswererInfo:
        return AnswererInfo(
            name=gettext("Word definition"),
            description=gettext("Show a concise definition for a single word"),
            keywords=self.keywords,
            examples=["define example", "define serendipity"],
        )

    def answer(self, query: str) -> list[BaseAnswer]:
        parts = query.strip().split(maxsplit=1)
        if len(parts) == 2 and parts[0].lower() == "define":
            word = parts[1].strip().strip('"').strip("'")
        elif len(parts) == 1 and _WORD_RE.match(parts[0]):
            word = parts[0]
        else:
            return []

        if not word or not _WORD_RE.match(word):
            return []

        url = "https://api.duckduckgo.com/?" + urlencode(
            {"q": f"define {word}", "format": "json", "no_redirect": 1}
        )
        try:
            resp = get(url, timeout=3.0)
            data = resp.json()
        except Exception:  # pylint: disable=broad-except
            return []

        definition = data.get("AbstractText") or data.get("Definition")
        if not definition:
            related = data.get("RelatedTopics") or []
            for topic in related:
                if isinstance(topic, dict) and topic.get("Text"):
                    definition = topic["Text"]
                    break

        if not definition:
            return []

        source = data.get("AbstractSource") or "DuckDuckGo"
        heading = data.get("Heading") or word
        return [Answer(answer=f"{heading}: {definition}", url=data.get("AbstractURL") or "", infobox=source)]