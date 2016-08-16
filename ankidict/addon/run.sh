#!/usr/bin/env bash
killall anki
set -e  # exit the script if any of the following commands fails
tidy -errors -q review.html
sass style.sass style.css
anki 2>&1 > /dev/null &
