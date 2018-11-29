#!/bin/bash

if [ $# -ne 4 ]; then
    echo 'Requires: path or alias to your Lighthouse, url, output filename, webdriver'
    exit 1
fi
mkdir -p tmp/$3 \
$1 $2 \
--only-categories=accessibility \
--no-enable-error-reporting \
--disable-device-emulation \
--chrome-flags="--headless --window-size=1300,600 --no-sandbox --disable-gpu" \
--output="json" \
--output-path="$(pwd)/tmp/$3.json";
python3 $(pwd)/openassessit/markdown.py \
--input-file="$(pwd)/tmp/$3.json" \
--output-file="$(pwd)/tmp/$3.md" \
--user-template-path="$(pwd)/../openassessit_templates/templates/";
mkdir -p tmp/$3/assets;
python3 $(pwd)/openassessit/capture.py \
--input-file="$(pwd)/tmp/$3.json" \
--assets-dir="$(pwd)/tmp/assets/" \
--sleep=4 \
--driver=$4