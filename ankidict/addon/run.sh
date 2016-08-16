#!/usr/bin/env bash
killall anki
sass style.sass style.css
anki 2>&1 > /dev/null &
