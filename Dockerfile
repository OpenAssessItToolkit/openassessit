# Parent image
# FROM stevedore-repo.oit.duke.edu/deb-base-17.10:latest

# TODO: Switching to ubuntu as base, moving stevador stuffinside this stand alone
#       file. Only diff between whats in the stevedor is we need to update to node 8

FROM ubuntu:17.10

LABEL name "openassessit"

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Python, Pip, Git, and Chromium
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.5 \
    python3-pip \
    && apt-get install -y npm chromium-browser imagemagick \
    && apt-get install -y git \
    && apt-get install -y zip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Lighthouse cli
RUN npm --global install -y lighthouse \
    && npm cache clean --force

# Clone OpenAssessIt repos
RUN git clone https://github.com/OpenAssessItToolkit/openassessit.git
RUN git clone https://github.com/OpenAssessItToolkit/openassessit_templates.git

# Install any needed packages specified in openassessits requirements.txt
RUN pip3 install --trusted-host pypi.python.org -r requirements.txt

# TODO: Install a webdriver https://www.blazemeter.com/blog/how-to-run-selenium-tests-in-docker

# create folder to save audit images in
RUN mkdir -p example/assets

# Define environment variable
ENV NAME openassessit

# TODO: Use Entrypoint so we can pass in variables
#       Probably move the whole run.sh into dockerfile
# ENTRYPOINT ['run.sh']