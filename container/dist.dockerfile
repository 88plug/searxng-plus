ARG CONTAINER_IMAGE_ORGANIZATION="88plug"
ARG CONTAINER_IMAGE_NAME="searxng-plus"

FROM localhost/$CONTAINER_IMAGE_ORGANIZATION/$CONTAINER_IMAGE_NAME:builder AS builder
FROM ghcr.io/searxng/base:searxng AS dist

COPY --chown=977:977 --from=builder /usr/local/searxng/.venv/ ./.venv/
COPY --chown=977:977 --from=builder /usr/local/searxng/searx/ ./searx/
COPY --chown=977:977 ./container/ ./
COPY --chown=977:977 ./searx/version_frozen.py ./searx/
COPY --chown=977:977 ./searx/favicons/favicons.toml ./favicons.toml.template

ARG CREATED="0001-01-01T00:00:00Z"
ARG VERSION="unknown"
ARG VCS_URL="unknown"
ARG VCS_REVISION="unknown"

LABEL org.opencontainers.image.created="$CREATED" \
    org.opencontainers.image.description="SearXNG-Plus: community fixes and engines from rejected PRs and graveyard issues." \
    org.opencontainers.image.documentation="https://github.com/88plug/searxng-plus" \
    org.opencontainers.image.licenses="AGPL-3.0-or-later" \
    org.opencontainers.image.revision="$VCS_REVISION" \
    org.opencontainers.image.source="$VCS_URL" \
    org.opencontainers.image.title="SearXNG-Plus" \
    org.opencontainers.image.url="https://github.com/88plug/searxng-plus" \
    org.opencontainers.image.version="$VERSION"

ENV __SEARXNG_VERSION="$VERSION" \
    __SEARXNG_SETTINGS_PATH="$__SEARXNG_CONFIG_PATH/settings.yml" \
    GRANIAN_PROCESS_NAME="searxng" \
    GRANIAN_INTERFACE="wsgi" \
    GRANIAN_HOST="::" \
    GRANIAN_PORT="8080" \
    GRANIAN_WEBSOCKETS="false" \
    GRANIAN_BLOCKING_THREADS="4" \
    GRANIAN_WORKERS_KILL_TIMEOUT="30s" \
    GRANIAN_BLOCKING_THREADS_IDLE_TIMEOUT="5m"

# "*_PATH" ENVs are defined in base images
VOLUME $__SEARXNG_CONFIG_PATH
VOLUME $__SEARXNG_DATA_PATH

EXPOSE 8080

ENTRYPOINT ["/usr/local/searxng/entrypoint.sh"]
