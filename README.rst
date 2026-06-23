.. SPDX-License-Identifier: AGPL-3.0-or-later

SearXNG-Plus
============

**SearXNG-Plus** is a community-maintained distribution of SearXNG that ships
fixes and features from open upstream issues and pull requests that were
rejected, closed without merge, or left unmerged.

- **Full documentation:** `docs/PLUS.md <docs/PLUS.md>`_
- **Repository:** https://github.com/88plug/searxng-plus
- **Container image:** ``ghcr.io/88plug/searxng-plus:latest``

Quick start with Docker:

.. code:: sh

   docker run --rm -d \
     -p 8080:8080 \
     -v searxng-plus-config:/etc/searxng \
     -v searxng-plus-data:/var/cache/searxng \
     ghcr.io/88plug/searxng-plus:latest

Or use the compose file in ``container/`` (image:
``ghcr.io/88plug/searxng-plus``).  Plus-added engines are **enabled by default**
on first run — see `docs/PLUS.md <docs/PLUS.md>`_ for release rounds and the
defaults policy.

----

.. _metasearch engine: https://en.wikipedia.org/wiki/Metasearch_engine
.. _Installation guide: https://docs.searxng.org/admin/installation.html
.. _Configuration guide: https://docs.searxng.org/admin/settings/index.html
.. _CONTRIBUTING: https://github.com/searxng/searxng/blob/master/CONTRIBUTING.rst
.. _LICENSE: https://github.com/searxng/searxng/blob/master/LICENSE

.. figure:: https://raw.githubusercontent.com/searxng/searxng/master/client/simple/src/brand/searxng.svg
   :target: https://searxng.org
   :alt: SearXNG
   :width: 512px


SearXNG is a `metasearch engine`_. Users are neither tracked nor profiled.

.. image:: https://img.shields.io/badge/organization-3050ff?style=flat-square&logo=searxng&logoColor=fff&cacheSeconds=86400
   :target: https://github.com/searxng
   :alt: Organization

.. image:: https://img.shields.io/badge/documentation-3050ff?style=flat-square&logo=readthedocs&logoColor=fff&cacheSeconds=86400
   :target: https://docs.searxng.org
   :alt: Documentation

.. image:: https://img.shields.io/github/license/searxng/searxng?style=flat-square&label=license&color=3050ff&cacheSeconds=86400
   :target: https://github.com/searxng/searxng/blob/master/LICENSE
   :alt: License

.. image:: https://img.shields.io/github/commit-activity/y/searxng/searxng/master?style=flat-square&label=commits&color=3050ff&cacheSeconds=3600
   :target: https://github.com/searxng/searxng/commits/master/
   :alt: Commits

.. image:: https://img.shields.io/weblate/progress/searxng?server=https%3A%2F%2Ftranslate.codeberg.org&style=flat-square&label=translated&color=3050ff&cacheSeconds=86400
   :target: https://translate.codeberg.org/projects/searxng/
   :alt: Translated

Setup
=====

To install SearXNG, see `Installation guide`_.

To fine-tune SearXNG, see `Configuration guide`_.

Further information on *how-to* can be found `here <https://docs.searxng.org/admin/index.html>`_.

Connect
=======

If you have questions or want to connect with others in the community:

- `#searxng:matrix.org <https://matrix.to/#/#searxng:matrix.org>`_

Contributing
============

See CONTRIBUTING_ for more details.

License
=======

This project is licensed under the GNU Affero General Public License (AGPL-3.0).
See LICENSE_ for more details.
