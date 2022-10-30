FROM python:3

RUN apt-get update
RUN apt-get -y install wget systemctl

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY Makefile .

COPY database_scheme database_scheme
COPY lifestat lifestat
COPY settings settings



