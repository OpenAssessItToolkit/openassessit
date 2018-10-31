#!/bin/bash

lighthouse $1 \
--only-categories=accessibility \
--disable-device-emulation \
--no-enable-error-reporting \
--output="json" \
--output-path="/app/example/$2.json" \
--chrome-flags="--headless --window-size=1300,600 --no-sandbox --disable-gpu";
python3 /app/openassessit/openassessit/markdown.py \
--input-file="/app/example/$2.json" \
--output-file="/app/example/$2.md" \
--user-template-path="/app/openassessit_templates/templates/";
python3 /app/openassessit/openassessit/capture.py \
--input-file="/app/example/$2.json" \
--assets-dir="/app/example/assets/" \
--sleep=4 \
--driver=firefox