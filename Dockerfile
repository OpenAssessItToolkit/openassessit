# Parent image
FROM ubuntu:18.10

LABEL name "openassessit"
LABEL maintainer Joel Crawford-Smith <jhc36@duke.edu>
LABEL version "1"
LABEL release "1"
LABEL summary "OpenAssessIt Quickstart"
LABEL Description "OpenAssessIt Process JSON Lighthouse reports into markdown files with images of failing items."

ENV DEBIAN_FRONTEND noninteractive


# Set the working directory to /app
WORKDIR /app

# Install Python, Pip, Git, and Chromium
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils \
    python3-setuptools \
    python3.5 \
    python3-pip \
    && apt-get install -y npm chromium-browser imagemagick \
    && apt-get install -y git \
    && apt-get install -y wget \
    && apt-get install -y zip \
    && apt-get install -y vim \
    && apt-get install -y firefox \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Lighthouse cli
RUN npm --global install -y lighthouse@^3.2.1 \
    && npm cache clean --force

# Clone OpenAssessIt repos
RUN git clone https://github.com/OpenAssessItToolkit/openassessit.git -b develop
RUN git clone https://github.com/OpenAssessItToolkit/openassessit_templates.git

# Install any needed packages specified in openassessits requirements.txt
RUN pip3 install wheel
RUN pip3 install --trusted-host pypi.python.org -r openassessit/requirements.txt

# TODO: Install a webdriver https://www.blazemeter.com/blog/how-to-run-selenium-tests-in-docker

# Gecko Driver
RUN wget -q "https://github.com/mozilla/geckodriver/releases/download/v0.23.0/geckodriver-v0.23.0-linux64.tar.gz" -O /tmp/geckodriver.tgz
RUN tar -xvzf /tmp/geckodriver.tgz
RUN rm /tmp/geckodriver.tgz
RUN chmod +x geckodriver
RUN mv geckodriver /usr/bin/

# Chrome Driver
RUN wget -q "https://chromedriver.storage.googleapis.com/2.43/chromedriver_linux64.zip" -O /tmp/chromedriver.zip
RUN unzip /tmp/chromedriver.zip
RUN rm /tmp/chromedriver.zip
RUN chmod +x chromedriver
RUN mv chromedriver /usr/bin/

# Define environment variable
ENV NAME openassessit

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]