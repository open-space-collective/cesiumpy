######################################################################################################################################################

# @project        CesiumPy
# @file           Dockerfile
# @license        Apache 2.0

######################################################################################################################################################

# Base

FROM python:3.9-slim-buster as base

## Update pip

RUN pip install --upgrade pip==20.2

## Configure working directory

WORKDIR /workspace

######################################################################################################################################################

# Production dependencies

FROM base as prod-deps

## Install dependencies

COPY requirements.txt .
RUN pip install -r requirements.txt

## Copy and install library

COPY . .
RUN pip install .

######################################################################################################################################################

# Production image

FROM base as prod

LABEL maintainer="lucas.bremond@gmail.com"

## Install iPython

RUN pip install ipython

## Add library

COPY --from=prod-deps /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=prod-deps /usr/local/bin /usr/local/bin

## Add license

COPY LICENSE .

## Configure entrypoint

CMD [ "ipython" ]

######################################################################################################################################################

# Development image

FROM mcr.microsoft.com/vscode/devcontainers/python:0-3.9 as dev

ARG NODE_VERSION="none"
RUN if [ "${NODE_VERSION}" != "none" ]; then su vscode -c "umask 0002 && . /usr/local/share/nvm/nvm.sh && nvm install ${NODE_VERSION} 2>&1"; fi

RUN pip install ipython

COPY requirements-dev.txt /tmp/pip-tmp/
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements-dev.txt \
   && rm -rf /tmp/pip-tmp

COPY requirements.txt /tmp/pip-tmp/
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
   && rm -rf /tmp/pip-tmp

ENV PYTHONPATH /workspace

######################################################################################################################################################
