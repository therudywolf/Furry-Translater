# UWU Translator — Web (static site + LLM reverse proxy)
FROM nginx:1.27-alpine

# Static assets only (no config.js, no .env, no infra files).
COPY forestchat.html styles.css /usr/share/nginx/html/
COPY js/ /usr/share/nginx/html/js/

# nginx site template (envsubst at startup) + frontend config renderer.
COPY docker/default.conf.template /etc/nginx/templates/default.conf.template
COPY docker/40-render-config.sh /docker-entrypoint.d/40-render-config.sh

# Normalize line endings (Windows checkouts) and make the hook executable.
RUN sed -i 's/\r$//' /docker-entrypoint.d/40-render-config.sh \
    && chmod +x /docker-entrypoint.d/40-render-config.sh

# Only substitute LLM_* vars in templates; leave nginx's own $variables intact.
ENV NGINX_ENVSUBST_FILTER=LLM_

EXPOSE 80

# Lightweight healthcheck on the static index.
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
    CMD wget -qO- http://127.0.0.1/ >/dev/null 2>&1 || exit 1
