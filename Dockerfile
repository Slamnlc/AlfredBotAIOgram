FROM python:3.8

WORKDIR /src
RUN mkdir /src/images
RUN apt-get install language-pack-en-base
COPY requirements.txt /src/requirements.txt
RUN pip install -r requirements.txt
COPY . /src