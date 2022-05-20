#!/bin/bash

if [ $# -ne 4 ]; then
    echo 'Requires: path or alias to your Lighthouse, url, output filename, webdriver'
    exit 1
fi
mkdir -p $(pwd)/tmp/$3;
$1 $2 \
--no-enable-error-reporting \
--preset=desktop \
--only-categories=accessibility \
--chrome-flags="--headless --window-size=1300,600 --no-sandbox --disable-gpu --preset=desktop" \
--output="json" \
--output-path="$(pwd)/tmp/$3/$3.json";
python3 -m openassessit.markdown \
--input-file="$(pwd)/tmp/$3/$3.json" \
--output-file="$(pwd)/tmp/$3/$3.md" \
--user-template-path="$(pwd)/../openassessit_templates/templates/";
python3 -m openassessit.to_html \
--input-file="$(pwd)/tmp/$3/$3.md" \
--output-file="$(pwd)/tmp/$3/$3.html" \
--user-template-path="$(pwd)/../openassessit_templates/templates/";
mkdir -p $(pwd)/tmp/$3/assets;
python3 -m openassessit.capture \
--input-file="$(pwd)/tmp/$3/$3.json" \
--assets-dir="$(pwd)/tmp/$3/assets/" \
--sleep=4 \
--driver=$4;
