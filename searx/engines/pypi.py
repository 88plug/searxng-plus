# SPDX-License-Identifier: AGPL-3.0-or-later
"""pypi.org"""

from urllib.parse import urlencode
from dateutil import parser

from lxml import html
from searx.utils import (
    eval_xpath_getindex,
    eval_xpath_list,
    extract_text,
)

# about
about = {
    "website": "https://pypi.org",
    "wikidata_id": "Q2984686",
    "official_api_documentation": "https://warehouse.readthedocs.io/api-reference/index.html",
    "use_official_api": False,
    "require_api_key": False,
    "results": "HTML",
}

categories = ['it', 'packages']


# engine dependent config
first_page_num = 1
base_url = "https://pypi.org"
search_url = base_url + '/search/?{query}'


def request(query, params):
    args = {
        "q": query,
        "page": params['pageno'],
    }
    params['url'] = search_url.format(query=urlencode(args))
    return params


def response(resp):
    results = []
    dom = html.fromstring(resp.text)
    for entry in eval_xpath_list(dom, '//a[@class="package-snippet"]'):
        url = base_url + extract_text(eval_xpath_getindex(entry, './@href', 0))  # type: ignore
        title = extract_text(eval_xpath_getindex(entry, './h3/span[@class="package-snippet__name"]', 0, default=""))
        version = extract_text(
            eval_xpath_getindex(entry, './h3/span[@class="package-snippet__version"]', 0, default="")
        )
        created_at = extract_text(
            eval_xpath_getindex(entry, './h3/span[@class="package-snippet__created"]', 0, default="")
        )
        content = extract_text(eval_xpath_getindex(entry, './p[@class="package-snippet__description"]', 0, default=""))
        published_date = None
        if created_at:
            try:
                published_date = parser.parse(created_at)
            except (ValueError, TypeError, parser.ParserError):
                pass
        results.append(
            {
                "template": "packages.html",
                "url": url,
                "title": title,
                'package_name': title,
                "content": content,
                "version": version,
                'publishedDate': published_date,
            }
        )

    return results
