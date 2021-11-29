# Parent image
FROM ubuntu:20.04

LABEL name "openassessit"
LABEL maintainer Joel Crawford-Smith <jhc36@duke.edu>
LABEL version "1"
LABEL release "1"
LABEL summary "OpenAssessIt Quickstart"
LABEL Description "OpenAssessIt Process JSON Lighthouse reports into markdown files with images of failing items."

ENV DEBIAN_FRONTEND noninteractive


# Set the working directory to /app
WORKDIR /app

# Install apps
RUN apt-get update && apt-get install -y \
  apt-transport-https \
  ca-certificates \
  curl \
  gnupg \
  --no-install-recommends \
  && curl -sSL https://deb.nodesource.com/setup_12.x | bash - \
  && curl -sSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
  && echo "deb https://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
  && apt-get update && apt-get install -y \
  google-chrome-stable \
  fontconfig \
  fonts-ipafont-gothic \
  fonts-wqy-zenhei \
  fonts-thai-tlwg \
  fonts-kacst \
  fonts-symbola \
  fonts-noto \
  fonts-freefont-ttf \
  nodejs \
  wget \
  git \
  firefox \
  python3-setuptools \
  python3-pip \
  zip \
  unzip \
  --no-install-recommends \
  && apt-get purge --auto-remove -y curl gnupg \
  && rm -rf /var/lib/apt/lists/*

# Install Lighthouse cli
RUN npm --global install -y lighthouse@6.5.0 \
    && npm cache clean --force

# Clone OpenAssessIt repos
RUN git clone https://github.com/OpenAssessItToolkit/openassessit.git
RUN git clone https://github.com/OpenAssessItToolkit/openassessit_templates.git

# Install any needed packages specified in openassessits requirements.txt
RUN pip3 install wheel
RUN pip3 install -r openassessit/requirements.txt

# Gecko Driver
RUN wget -q "https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz" -O /tmp/geckodriver.tgz
RUN tar -xvzf /tmp/geckodriver.tgz
RUN rm /tmp/geckodriver.tgz
RUN chmod +x geckodriver
RUN mv geckodriver /usr/bin/

# Chrome Driver
RUN wget -q "https://chromedriver.storage.googleapis.com/2.44/chromedriver_linux64.zip" -O /tmp/chromedriver.zip
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
