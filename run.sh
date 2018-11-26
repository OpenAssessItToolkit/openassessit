#!/bin/bash

if [ $# -ne 4 ]; then
    echo 'Requires, url, output filename, path or alias to your Lighthouse, webdriver'
    exit 1
fi
$3 $1 \

--only-categories=accessibility \
--no-enable-error-reporting \
--output="json" \
--output-path="$(pwd)/tmp/$2.json" \
--chrome-flags="--headless --window-size=1300,600 --no-sandbox --disable-gpu --disable-device-emulation";
python3 $(pwd)/openassessit/markdown.py \
--input-file="$(pwd)/tmp/$2.json" \
--output-file="$(pwd)/tmp/$2.md" \
--user-template-path="$(pwd)/../openassessit_templates/templates/";
mkdir -p tmp/assets;
python3 $(pwd)/openassessit/capture.py \
--input-file="$(pwd)/tmp/$2.json" \
--assets-dir="$(pwd)/tmp/assets/" \
--sleep=4 \
--driver=$4