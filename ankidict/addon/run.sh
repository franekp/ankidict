#!/usr/bin/env bash
set -e
killall anki
tidy -errors -q review.html || exit 1
sass style.sass style.css
anki 2>&1 > /dev/null &
