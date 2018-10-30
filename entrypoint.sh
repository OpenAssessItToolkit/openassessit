#!/bin/bash

lighthouse $1 \
--only-categories=accessibility \
--disable-device-emulation \
--output="json" \
--output-path="/app/example/$2.json" \
--chrome-flags="--headless --window-size=1300,600";
python3 /openassessit/markdown.py \
--input-file="/app/example/$2.json" \
--output-file="/app/example/$2.md" \
--user-template-path="/app/openassessit_templates/templates/";
mkdir -p example/assets;
python3 $/openassessit/capture.py \
--input-file="/app/example/$2.json" \
--assets-dir="/app/example/assets/" \
--sleep=4 \
--driver=firefox