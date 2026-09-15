#!/bin/bash
# pager.example.sh — example RALPH_MANAGER_PAGER hook.
# The overseer calls this with the message as $1. Wire it to whatever paging
# channel you own: a chat-bot webhook, a push service, email, SMS gateway.
# Keep the token on THIS box, in an env file the script sources — never in
# the overseer repo, logs, or crontab.
set -u
MSG="${1:?usage: pager.sh <message>}"

# Example: generic webhook (fill in your own URL via env).
# : "${PAGER_WEBHOOK_URL:?set PAGER_WEBHOOK_URL}"
# curl -sS -X POST "$PAGER_WEBHOOK_URL" \
#   -H 'Content-Type: application/json' \
#   -d "$(jq -nc --arg text "$MSG" '{text:$text}')" >/dev/null

echo "PAGE: $MSG"
