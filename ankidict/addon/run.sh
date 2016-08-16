#!/usr/bin/env bash
killall anki
set -e  # exit the script if any of the following commands fails
tidy -errors -q review.html  # html linter
sass style.sass style.css  # sass preprocessor
postcss -u autoprefixer style.css -o style.css  # autoprefixer
anki 2>&1 > /dev/null &
