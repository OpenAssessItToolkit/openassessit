# Parent image
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
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Lighthouse cli
RUN npm --global install -y lighthouse \
      && npm cache clean --force

# Clone OpenAssessIt repos
RUN git clone https://github.com/OpenAssessItToolkit/openassessit.git
RUN git clone https://github.com/OpenAssessItToolkit/openassessit_templates.git

# Install any needed packages specified in openassessits requirements.txt
RUN pip3 install --trusted-host pypi.python.org -r openassessit/requirements.txt

# create folder to save audit images in
RUN mkdir -p example/assets

# Define environment variable
ENV NAME openassessit

# Run OpenAssessIt markdown.py and capture.py when the container launches
CMD ["sh", "run.sh https://cats.com cats lighthouse"]

ENTRYPOINT ['run.sh']

# move run.sh into dockerfile