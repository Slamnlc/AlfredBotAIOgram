FROM python:latest

WORKDIR /src
RUN -e TZ=Europe/Kiev
RUN mkdir /images
RUN apt-get update
RUN apt-get -y install cron
RUN apt-get install -y locales locales-all
RUN update-locale LANG=ru_RU.UTF-8
ENV LC_ALL ru_RU.UTF-8
ENV LANG ru_RU.UTF-8
ENV LANGUAGE ru_RU.UTF-8
COPY requirements.txt /src/requirements.txt
RUN pip install -r requirements.txt
COPY . /src