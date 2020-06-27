FROM ubuntu:18.04

MAINTAINER Carlos Rosas <fantaso.code@gmail.com>

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
ENV LANGUAGE en_US.UTF-8


# OS: [dependencies]
RUN apt-get update && apt-get -y install --no-install-recommends \
    python3 python3-pip python3-setuptools \
    wget \
    # Firefox & Geckdriver Prerequisites
    unzip xvfb libxi6 libgconf-2-4 \
    firefox \
    # Erasing apt-get cache
    && rm -rf /var/lib/apt/lists/*

# OS: [dependencies:geckodriver]
ARG GECKODRIVER_VERSION=v0.26.0
RUN wget https://github.com/mozilla/geckodriver/releases/download/${GECKODRIVER_VERSION}/geckodriver-${GECKODRIVER_VERSION}-linux64.tar.gz  \
    && tar xzf geckodriver-${GECKODRIVER_VERSION}-linux64.tar.gz  \
    && mv geckodriver /usr/bin/geckodriver  \
    && rm geckodriver-${GECKODRIVER_VERSION}-linux64.tar.gz

# OS: [User]
RUN useradd -m app

# APP: [dependencies]
COPY requirements.txt /home/app
RUN pip3 install --no-cache-dir -r /home/app/requirements.txt \
    && rm /home/app/requirements.txt

# APP: [repository]
COPY --chown=app:app tradefest_scraper /home/app

# THIS IS NOT NEEDED WHEN NOT USING THE
#   VOLUME TO MAP THE SCRAPPED DATA INTO THE LOCAL MACHINE
RUN mkdir -p /home/app/output/feeds \
    && mkdir -p /home/app/output/logs \
    && mkdir -p /home/app/output/media \
     && chown -R app:app /home/app/output


#################################
###  Get ready, set & Python  ###
#################################
USER app
WORKDIR /home/app/tradefest_scraper
CMD ["scrapy", "crawl", "tradefest"]
