# Suggested configuration for an accessibility audit
The OpenAssesIt Toolkits suite of projects are meant to be run independently or as a suite. Below is a suggested configuration. This project can work on all audit categories, but current efforts are focused on the accessibility audits.

### Prerequisites

1. Don't be intimidated, you can do this.

2. Verify that [Chrome Lighthouse](https://github.com/GoogleChrome/lighthouse/) is [installed](https://github.com/GoogleChrome/lighthouse#using-the-node-cli) `lighthouse --version`
3. Verify that [Python](https://www.python.org/) is [installed](https://realpython.com/installing-python/), preferaby Python 3.6+, `python --version` or `python3 --version`
4. Verify that [PIP](https://pypi.org/project/pip/) is [installed](https://www.makeuseof.com/tag/install-pip-for-python/) `pip --version` (Note Pip already comes with Python 2.7.9+ and 3.4+)
5. Verify that a webdriver is [installed](https://pypi.org/project/selenium/#drivers) (Firefox gecko or Chrome)
6. Run `pip install -r requirements.txt` from the root of this repo to install Selenium, Jinja2, and Pillow.
7. Read the README.md files.

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

## Notes

1. If you want to change the order of the audits create a custom lighthouse config, by changing the order of the `[categories][accessibility][auditRefs]`

1. The report creates images from elements listed in 'color-contrast', 'link-name', 'button-name', image-alt', 'input-image-alt', 'iframe-title', and 'label' audits.

2. There is a rare [bug in Axe-core that creates invalid selectors](https://github.com/dequelabs/axe-core/issues/1165) in some edge case scenarios. When that issue is fixed in Axe-core it will get included in Lighthouse, then this issue will go away. Skipped images are logged and printed to the console.

This project is only possible because of [ihadgraft](https://github.com/ihadgraft)'s generous donation of his expertise, time, and patience with [joelhsmith](https://github.com/joelhsmith).  Thank you Iain!
