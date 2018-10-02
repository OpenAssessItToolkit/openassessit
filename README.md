# Suggested configuration for an accessibility audit
The OpenAssesIt Toolkits suite of projects are meant to be run independently or as a suite. Below is a suggested configuration. This project can work on all audit categories, but current efforts are focused on the accessibility audits.

### Prerequisites 

1. Install [Chrome Lighthouse](https://github.com/GoogleChrome/lighthouse/), Python _2.7_, and a webdriver.

2. Read the README.md files.

## Setup

From your projects directory:

__1) Install requirements:__

```
pip install -r requirements.txt
```

__2) Clone OpenAssessIt and OpenAssessIt Templates:__

```
git clone https://github.com/OpenAssessItToolkit/openassessit.git
```
```
git clone https://github.com/OpenAssessItToolkit/openassessit_templates.git
```

## Run 

__1) Create a Lighthouse json accessibility audit file to import__


```
lighthouse https://cats.com \
--only-categories=accessibility \
--disable-device-emulation \
--output=json \
--output-path=catsaudit.json \
--chrome-flags="--headless --window-size=1300,600"
```
<sub>Or use these [custom Lighthouse audit recipes](https://github.com/joelhsmith/audit_recipes)</sub>

__2) Run Lighthouse to Markdown__

Converts the json file to markdown.

```
python openassessit/markdown.py \
--input-file="catsaudit.json" \
--output-file="catsaudit.md" \
--user-template-path="/abs/path/to/openassessit_templates/templates/"
```

__3) Run Capture Assets__

Looks for failed audit items in the json file and create a screenshots of each offending element and saves them in an 'assets' folder.

```
mkdir assets
```

```
python openassessit/capture.py \
--input-file="/abs/path/to/catsaudit.json" \
--assets-dir="/abs/path/to/assets/" \
--sleep=1 \
--driver=firefox
```

## Make friends and influence people


```
open catsaudit.md
```

Your markdown file is complete. You can use it as-is, or augment the content with additional custom help text.  I usually use MacDown and save them out as html files and host them on GitHub pages.
 




