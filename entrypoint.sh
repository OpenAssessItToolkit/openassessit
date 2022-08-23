#!/bin/bash

mkdir -p /tmp/$2/assets;
cd openassessit;
CHROME_PATH=/usr/bin/chromedriver lighthouse $1 --only-categories=accessibility --no-enable-error-reporting --emulated-form-factor=none --chrome-flags="--headless --window-size=1300,600 --no-sandbox --disable-gpu" --output="json" --output-path="/tmp/$2/$2.json";
python3 -m openassessit.markdown --input-file="/tmp/$2/$2.json" --output-file="/tmp/$2/$2.md" --user-template-path="/app/openassessit_templates/templates/";
python3 -m openassessit.to_html --input-file="/tmp/$2/$2.md" --output-file="/tmp/$2/$2.html" --user-template-path="/app/openassessit_templates/templates/";
python3 -m openassessit.capture --input-file="/tmp/$2/$2.json" --assets-dir="/tmp/$2/assets/" --sleep=4 --driver=$3;
zip -r /tmp/$2.zip /tmp/$2;