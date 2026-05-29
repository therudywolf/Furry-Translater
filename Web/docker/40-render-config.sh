#!/bin/sh
# Render the frontend config.js from environment at container start.
# Runs via the official nginx image's /docker-entrypoint.d mechanism,
# before nginx starts. Contains NO secret — the API key stays in nginx.
set -eu

: "${LLM_MODEL:=google/gemma-4-e2b}"
# '=' (not ':=') so an explicitly-empty value from .env is preserved.
: "${LLM_REASONING_EFFORT=}"
: "${LLM_MAX_TOKENS:=600}"

cat > /usr/share/nginx/html/config.js <<EOF
// Generated at container start from environment — do not edit.
window.API_BASE_URL = '/api/llm';
window.MODEL_NAME = '${LLM_MODEL}';
window.API_KEY = '';
window.REASONING_EFFORT = '${LLM_REASONING_EFFORT}';
window.MAX_TOKENS = ${LLM_MAX_TOKENS};
window.CHAT_HISTORY_LIMIT = 20;
window.REQUEST_TIMEOUT_MS = 60000;
EOF

echo "[entrypoint] rendered config.js (proxy mode, model=${LLM_MODEL}, reasoning_effort=${LLM_REASONING_EFFORT})"
