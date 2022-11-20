FROM python:3

RUN apt-get update
RUN apt-get -y install wget systemctl

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY Makefile .

COPY lifestat lifestat
COPY settings settings
COPY init_test.sql .
COPY data_test.sql .
RUN mkdir ~/.postgresql
COPY root.crt /root/.postgresql/root.crt

EXPOSE 8000

CMD [ "make" , "run" ]