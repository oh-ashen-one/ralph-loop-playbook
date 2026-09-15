#!/bin/bash
# install.sh [project_root ...] — register hourly check-ins + 5-min watch for
# the given projects in the loop box's crontab. Idempotent (marker block).
set -u
DIR="${OVERSEER_DIR:-$(cd "$(dirname "$0")" && pwd)}"
MARK_BEGIN="# >>> ralph-overseer >>>"
MARK_END="# <<< ralph-overseer <<<"

LINES="$MARK_BEGIN"
for ROOT in "$@"; do
  NAME="$(basename "$ROOT")"
  LINES="$LINES
7 * * * * /bin/bash $DIR/checkin.sh '$ROOT' >> /tmp/ralph-overseer-$NAME.log 2>&1
*/5 * * * * /bin/bash $DIR/watch.sh '$ROOT' >> /tmp/ralph-overseer-$NAME.log 2>&1"
done
LINES="$LINES
$MARK_END"

(crontab -l 2>/dev/null | sed "/$(printf '%s' "$MARK_BEGIN" | sed 's/[][\.*^$/]/\\&/g')/,/$(printf '%s' "$MARK_END" | sed 's/[][\.*^$/]/\\&/g')/d"; printf '%s\n' "$LINES") | crontab -
echo "installed for: $*"
crontab -l | sed -n "/$MARK_BEGIN/,/$MARK_END/p"
