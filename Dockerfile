FROM ubuntu:bionic

MAINTAINER Carlos Rosas <fantaso.code@gmail.com>

ENV PYTHONUNBUFFERED=1
ENV LANG=C.UTF-8
ENV LANGUAGE=en_US.UTF-8

#ARG GECKODRIVER=v0.26.0


###################
###  OS config  ###
###################
###  Build dependencies  ###
RUN apt-get update && apt-get install -y \
    python3 python3-pip \
    wget \
    # Firefox & Geckdriver Prerequisites  ###
    unzip xvfb libxi6 libgconf-2-4 \
    firefox && \
    # Erasing apt-get cache
    rm -rf /var/lib/apt/lists/*

## Geckodriver
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz && \
    tar xzf geckodriver-v0.26.0-linux64.tar.gz && \
    mv geckodriver /usr/bin/geckodriver && \
    rm geckodriver-v0.26.0-linux64.tar.gz

###  Create user to host the app with (-m) home directory
RUN useradd -m app


####################
###  App config  ###
####################
WORKDIR /home/app

###  Copy entire django app and repo  ###
COPY . .

###  Install app dependencies  ###
RUN pip3 install --no-cache-dir -r requirements.txt


#################################
###  Get ready, set & Python  ###
#################################
#USER app
WORKDIR /home/app/tradefest_scraper/tradefest_scraper
ENTRYPOINT ["scrapy", "crawl", "tradefest"]

