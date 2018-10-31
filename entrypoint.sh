#!/bin/bash

mkdir -p /app/assessments/$2/assets;
lighthouse $1 \
--only-categories=accessibility \
--disable-device-emulation \
--no-enable-error-reporting \
--output="json" \
--output-path="/app/assessments/$2/$2.json" \
--chrome-flags="--headless --window-size=1300,600 --no-sandbox --disable-gpu";
python3 /app/openassessit/openassessit/markdown.py \
--input-file="/app/assessments/$2/$2.json" \
--output-file="/app/assessments/$2/$2.md" \
--user-template-path="/app/openassessit_templates/templates/";
python3 /app/openassessit/openassessit/capture.py \
--input-file="/app/assessments/$2/$2.json" \
--assets-dir="/app/assessments/$2/assets/" \
--sleep=4 \
--driver=firefox;
zip -r assessments/$2/$2.zip /app/assessments/$2
