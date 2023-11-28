# OpenAssessIt

This project consumes a [Chrome Lighthouse](https://developers.google.com/web/tools/lighthouse/) JSON report and outputs a human readable version with screenshots of failing elements and suggestions on how to fix issues. The Accessibility portion of Chrome Lighthouse is largely sourced from [Deque's Axe-core](https://github.com/dequelabs/axe-core) engine.

The project is written in Python. But, no Python experience is needed to use this project in its Docker configuration. If you do know Python, we would love your help.

__Below is a link to a quick video that explains what OpenAssessIt does for you:__

https://youtu.be/xqAs0RMc1Rs


# Suggested configuration for an accessibility audit

This project can work on all audit categories, but current efforts are focused on the accessibility audits.

## Two options to get started:

__Option 1. Run in local Docker container (Docker version no longer works on Mac due to ARM vs X86 architecture differences)__

_OR_

__Option 2. Manually install prerequisites and run natively__

---

### Option 1. Run in Docker container

This is the easiest way to get set up. No stress, no mess.

#### Prerequisites

Download and Install Docker for your OS:

[Docker for Mac](https://docs.docker.com/docker-for-mac/install/)

[Docker for Windows](https://docs.docker.com/docker-for-windows/install/)

NOTE: Currently Docker container verions is still using the computers local headless version of Chrome instead of the version inside the Docker container.  Until we get that ironed out, please verify that a webdriver is [installed](https://pypi.org/project/selenium/#drivers) (Firefox gecko or Chrome) and verify that [Chrome Lighthouse](https://github.com/GoogleChrome/lighthouse/) is [installed](https://github.com/GoogleChrome/lighthouse#using-the-node-cli) `lighthouse --version`

#### Setup

Download OpenAssessIt:

```
git clone https://github.com/OpenAssessItToolkit/openassessit.git
```

Change directory:

```
cd openassessit
```

#### Run it

Docker builds a tiny 1GB Docker Image (sorta like a VM) and installs everything inside that Container for you. _It does not install any packages on your local computer_.

Build the latest OpenAssessIt image:

_Note: It might take up to 5 minutes for it to download everything._

```
docker-compose build
```

Build the Container to run the assessment (You can run as many assessments as you want from this Image build).

docker-compose run openassessit [url] [foldername] [webdriver]

```
docker-compose run openassessit https://cats.com catshomepage chrome
```

When you are done, remove the Image and the Container.

```
docker-compose down --rmi all
```

The audit will automatically be copied into your `openassessit/tmp/` directory.


---

# _OR_

### Option 2. Manually install prerequisites and run locally


```
brew install node@16
brew link node@16
npm --global install -y lighthouse@10.4.0
brew install geckodriver
brew install chromedriver
```

Note: Works with [Lighthouse 10](https://github.com/GoogleChrome/lighthouse/releases/tag/v10.4.0)

1. [Start up a virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
2. Verify that [Chrome Lighthouse](https://github.com/GoogleChrome/lighthouse/) is [installed](https://github.com/GoogleChrome/lighthouse#using-the-node-cli) `lighthouse --version`
3. Verify that [Python](https://www.python.org/) is [installed](https://realpython.com/installing-python/), preferaby Python 3.6+, `python --version` or `python3 --version`
4. Verify that [PIP](https://pypi.org/project/pip/) is [installed](https://www.makeuseof.com/tag/install-pip-for-python/) `pip --version` (Note Pip already comes with Python 2.7.9+ and 3.4+)
5. Verify that a webdriver is [installed](https://pypi.org/project/selenium/#drivers) ([Firefox geckodriver 0.30.0](https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz)  or [Chrome 2.44](https://chromedriver.storage.googleapis.com/2.44/chromedriver_linux64.zip))
6. Run `pip install -r requirements.txt` from the root of this repo to install Selenium, Jinja2, and Pillow.
7. Read the README.md files.

#### Setup

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

#### Run

_Note: You could optionally use the run.sh file to run all these commands in serial._

__1) Create a Lighthouse json accessibility audit file to import__


```
lighthouse https://cats.com \
--only-categories=accessibility \
--preset=desktop \
--output=json \
--output-path=catsaudit.json \
--chrome-flags="--headless --window-size=1300,600"
```
Or use our [custom Lighthouse accessibility audit recipe](https://gist.github.com/joelhsmith/21bb103e987da65c67f6420488643380)

__2) Run Lighthouse to Markdown__

Converts the json file to markdown.

```
python -m openassessit.markdown \
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
python -m openassessit.capture \
--input-file="/abs/path/to/catsaudit.json" \
--assets-dir="/abs/path/to/assets/" \
--sleep=1 \
--driver=chrome
```


__4) Review the issues__

```
open catsaudit.md
```

__OR run all the commands together with the `run.sh` file__

```
chmod +x run.sh
```

Example: 

```
./run.sh lighthouse https:/cats.com/ catscom firefox
```

You can use it as-is, or augment the content with additional custom help text. It takes a real human to validate and prioritize accessibility issues.  We recommend that people perform the list of manual tests and the results.


The Markdown file works best with an editor compatible with "Markdown Extras" like __[MacDown](https://macdown.uranusjr.com/)__ then you can use it to export it to HTML from there.

Or...


__4) Convert MD to HTML after you are done editing it__

We have a built in Markdown to HTML converter. The header and footer of the HTML are also customizable in the openassessit_templates folder.

```
python3 -m openassessit.to_html  \
--input-file="/abs/path/to/catsaudit.md" \
--output-file="/abs/path/to/catsaudit.html" \
--user-template-path="/abs/path/to/openassessit_templates/templates/"
```

```
open catsaudit.html
```

When we are done, we host these assessments on GitHub pages.

---

## Make friends and influence people


### Notes

1. If you want to change the order of the audits in the Markdown file, create a [custom Lighthouse config](https://gist.github.com/joelhsmith/21bb103e987da65c67f6420488643380) and change the weight `[categories][accessibility][auditRefs][id][weight]`

2. The report creates images from elements listed in 'color-contrast', 'link-name', 'button-name', 'image-alt', 'input-image-alt', 'label', 'accesskeys', 'frame-title', 'duplicate-id', 'list', 'listitem', 'definition-list', 'dlitem'.

3. If there is a failing element in a visibly hidden element, it will take a screen shot of the coordinates of the failing element.  It does not know if the element is visible or not. As a result the screenshot will not always be what you expect it to be. Sometimes the screenshot being incorrect can be a helpful clue to debug the underlying problem.

4. For websites that require an exceptionally large amount of resources, you may need go into Docker's 'Advanced' preferences and increase it's resources.

This project is only possible because of [ihadgraft](https://github.com/ihadgraft)'s generous donation of his expertise, time, and patience with [joelhsmith](https://github.com/joelhsmith) and our other contributers:

* [drewstinnett](https://github.com/(https://github.com/ptrin))
* [ptrin](https://github.com/ptrin)
* [thegreenbot](https://github.com/thegreenbot)
