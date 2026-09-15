#!/bin/bash
# ensure_model.sh — guarantee OUR model identifier is loaded before a round.
#
# On a shared inference box a co-tenant's ensure-job can evict your model
# mid-run. Every subsequent iteration then fails with HTTP 400 for a model id
# that no longer exists, the restart ladder burns out, and the supervisor dies
# — while /v1/models still answers 200 because the SERVER is fine
# (FAILURES #79). This makes the loop self-healing instead of hand-fed.
#
#   ensure_model.sh [identifier] [weights]
#
# Additive only: it loads OUR identifier and never unloads anything, so a
# co-tenant's instance is left exactly as it is.
set -uo pipefail
IDENT="${1:-${QWEN_MODEL:-ralph-showcase}}"
WEIGHTS="${2:-${QWEN_WEIGHTS:-mlx-community/Qwen3.8-27B-8bit}}"
API="${QWEN_MODELS_URL:-http://127.0.0.1:1234/v1/models}"
CTX="${QWEN_CTX:-262144}"
export PATH="$HOME/.lmstudio/bin:$PATH"

models="$(curl -s --max-time 10 "$API" || echo "")"
if [[ -z "$models" ]]; then
  echo "ensure_model: model server unreachable at $API" >&2
  exit 1
fi
if grep -q "\"$IDENT\"" <<<"$models"; then
  exit 0
fi

echo "ensure_model: '$IDENT' is NOT loaded (evicted?) — reloading $WEIGHTS"
if ! command -v lms >/dev/null 2>&1; then
  echo "ensure_model: lms CLI not on PATH; cannot self-heal" >&2
  exit 1
fi
lms load "$WEIGHTS" --identifier "$IDENT" -c "$CTX" --gpu max -y >/dev/null 2>&1

for _ in $(seq 1 10); do
  sleep 3
  models="$(curl -s --max-time 10 "$API" || echo "")"
  if grep -q "\"$IDENT\"" <<<"$models"; then
    echo "ensure_model: '$IDENT' restored"
    exit 0
  fi
done
echo "ensure_model: FAILED to restore '$IDENT' — escalate to a human" >&2
exit 1
