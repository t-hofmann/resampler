FROM python:3-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN echo "installing prerequisites for 'xlsx to csv converter'" \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        libreoffice-calc \
        libreoffice-java-common \
        openjdk-17-jre \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN echo "installing prerequisites for executing python package 'samplerate'" \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        libsamplerate0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install numpy
RUN pip install samplerate

COPY ./fs_root/. /

WORKDIR /app
