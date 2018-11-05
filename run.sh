#!/bin/bash

if [ $# -ne 3 ]; then
    echo 'Requires, url, output filename, and path or alias to your Lighthouse install'
    exit 1
fi
$3 $1 \

lighthouse $1 \
--only-categories=accessibility \
--disable-device-emulation \
--output=json \
--output-path="$(pwd)/example/$2.json" \
--chrome-flags="--headless --window-size=1300,600"
--disable-device-emulation \
--output="json" \
--output-path="$(pwd)/example/$2.json" \
--chrome-flags="--headless --window-size=1300,600";
python3 $(pwd)/openassessit/markdown.py \
--input-file="$(pwd)/example/$2.json" \
--output-file="$(pwd)/example/$2.md" \
--user-template-path="$(pwd)/../openassessit_templates/templates/";
python3 $(pwd)/openassessit/capture.py \
--input-file="$(pwd)/example/$2.json" \
--assets-dir="$(pwd)/example/assets/" \
--sleep=4 \
--driver=firefox