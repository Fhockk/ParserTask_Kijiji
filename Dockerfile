FROM python:3

# set working directory
WORKDIR /usr/src/scrap

COPY ./app ./app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt