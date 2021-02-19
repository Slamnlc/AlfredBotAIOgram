FROM python:3.8

WORKDIR /src
RUN mkdir /src/images
RUN apt-get update
RUN apt-get -y install locales locales-all
RUN sed -i -e 's/# ru_RU.KOI8-R UTF-8/ru_RU.KOI8-R UTF-8/' /etc/locale.gen && locale-gen
COPY requirements.txt /src/requirements.txt
RUN pip install -r requirements.txt
COPY . /src