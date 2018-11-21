#!/bin/bash

mkdir -p /tmp/$2/assets;
lighthouse $1 \
--only-categories=accessibility \
--no-enable-error-reporting \
--output="json" \
--output-path="/tmp/$2/$2.json" \
--chrome-flags="--headless --window-size=1300,600 --no-sandbox --disable-gpu --disable-device-emulation";
python3 /app/openassessit/openassessit/markdown.py \
--input-file="/tmp/$2/$2.json" \
--output-file="/tmp/$2/$2.md" \
--user-template-path="/app/openassessit_templates/templates/";
python3 /app/openassessit/openassessit/capture.py \
--input-file="/tmp/$2/$2.json" \
--assets-dir="/tmp/$2/assets/" \
--sleep=4 \
--driver=$3;
zip -r /tmp/$2.zip /tmp/$2
