#!/usr/bin/env bash
killall anki
set -e  # exit the script if any of the following commands fails
tidy -errors -q review.html  # html linter
sass style.sass style.css  # sass preprocessor
postcss --use autoprefixer --use postcss-gradientfixer --replace style.css   # autoprefixer
anki 2>&1 > /dev/null &
