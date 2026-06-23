# SPDX-License-Identifier: AGPL-3.0-or-later
# pylint: disable=missing-module-docstring,missing-class-docstring,invalid-name

from searx.query import RawTextQuery

from tests import SearxTestCase


class TestRequireAllTerms(SearxTestCase):

    def test_bang_quotes_all_terms(self):
        q = RawTextQuery('!+ linux kernel security', [])
        self.assertEqual(q.getQuery(), '"linux" "kernel" "security"')

    def test_without_bang_unchanged(self):
        q = RawTextQuery('linux kernel security', [])
        self.assertEqual(q.getQuery(), 'linux kernel security')