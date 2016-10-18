#!/usr/bin/env bash
cd "$( dirname ${BASH_SOURCE[0]} )"
killall anki
set -e  # exit the script if any of the following commands fails
tidy -errors -q index.html  # html linter
sass style.sass style.css  # sass preprocessor
postcss --use autoprefixer --use postcss-gradientfixer --replace style.css   # autoprefixer

jsx app.jsx > app.js  # reactjs part

elm make elmapp/main.elm --output elmapp.js  # elm part

anki & #2>&1 > /dev/null &
