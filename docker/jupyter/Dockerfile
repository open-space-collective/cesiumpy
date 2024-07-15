# Apache License 2.0

ARG JUPYTER_NOTEBOOK_IMAGE_REPOSITORY=jupyter/scipy-notebook:x86_64-python-3.11.3

FROM ${JUPYTER_NOTEBOOK_IMAGE_REPOSITORY}

LABEL maintainer="vishwa@loftorbital.com"

# Set user to root

USER root

# Install Python utilities

RUN apt-get update \
    && apt-get install -y sudo curl git-lfs \
    && rm -rf /var/lib/apt/lists/*

RUN jupyter labextension install --no-build \
    @jupyterlab/shortcuts-extension

COPY --chown=${NB_UID}:${NB_GID} docker/jupyter/shortcuts-extension /home/jovyan/.jupyter/lab/user-settings/@jupyterlab/shortcuts-extension

# Install Toolkit dependencies

COPY requirements.txt README.md requirements-dev.txt setup.py /tmp/

RUN SETUPTOOLS_SCM_PRETEND_VERSION="0.0.0" \
    pip install -e /tmp/ \
    pip install -r \
    /tmp/requirements-dev.txt

# Restore user

USER ${NB_UID}

# Disable token

CMD [ "start-notebook.sh", "--NotebookApp.token=''" ]
