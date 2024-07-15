# Apache License 2.0

project_name := cesiumpy
project_version := $(shell git describe --tags --always)

image_registry := lucasbremond
image_url := $(image_registry)/$(project_name)
dev_image_url := $(image_url)-dev

service_name := $(project_name)
working_directory := /workspace

jupyter_image_url := $(image_url)-jupyter
jupyter_port := 9001
jupyter_python_version := 3.11

image: ## Build production image
	docker build \
		--target=prod \
		--tag=$(image_url) \
		--tag=$(image_url):$(project_version) \
		.
.PHONY: image

dev-image: ## Build development image
	docker build \
		--target=dev \
		--tag=$(dev_image_url) \
		--tag=$(dev_image_url):$(project_version) \
		.
.PHONY: dev-image

jupyter-image: ## Build Jupyter image
	docker build \
		--file="$(CURDIR)/docker/jupyter/Dockerfile" \
		--tag=$(jupyter_image_url):$(project_version) \
		--tag=$(jupyter_image_url):latest \
		.
.PHONY: jupyter-image

run: image ## Run container
	docker run \
		--name=$(service_name) \
		-it \
		--rm \
		$(image_url):$(project_version)
.PHONY: run

dev: dev-image ## Run development environment
	docker run \
		--name=$(service_name)-dev \
		-it \
		--rm \
		--volume="$(CURDIR):$(working_directory)" \
		--env="CESIUM_TOKEN=$(CESIUM_TOKEN)" \
		--workdir=$(working_directory) \
		$(dev_image_url):$(project_version) \
		/bin/bash
.PHONY: dev

jupyter-dev: jupyter-image ## Run Jupyter environment
	docker run \
	    --name=$(service_name)-jupyter-dev \
		-it \
		--rm \
		--user=root \
		--env="CESIUM_TOKEN=$(CESIUM_TOKEN)" \
		--publish=$(jupyter_port):8888 \
		--volume="$(CURDIR)/notebooks:/home/jovyan/work" \
		--volume="$(CURDIR):/opt/conda/lib/python$(jupyter_python_version)/site-packages/$(project_name)" \
		--workdir="/home/jovyan/work" \
		$(jupyter_image_url):$(project_version) \
		/bin/bash -c "chown -R jovyan:users /home/jovyan ; export PYTHONPATH="${PYTHONPATH}:/opt/conda/lib/python$(jupyter_python_version)/site-packages/$(project_name)" ; start-notebook.sh --ServerApp.token=''"

	@ sudo chown -R $(shell id -u):$(shell id -g) $(CURDIR)

.PHONY: jupyter-dev

check-style: dev-image ## Check code formatting
	docker run \
		--rm \
		--volume="$(CURDIR):$(working_directory)" \
		--workdir=$(working_directory) \
		$(dev_image_url):$(project_version) \
		/bin/bash -c "flake8"
.PHONY: check-style

check-types: dev-image ## Check types
	docker run \
		--rm \
		--volume="$(CURDIR):$(working_directory)" \
		--workdir=$(working_directory) \
		$(dev_image_url):$(project_version) \
		/bin/bash -c "mypy -p ccsds -p tests -p setup"
.PHONY: check-types

test: dev-image ## Run unit tests
	docker run \
		--rm \
		--volume="$(CURDIR):$(working_directory)" \
		--workdir=$(working_directory) \
		$(dev_image_url):$(project_version) \
		/bin/bash -c "pytest -svx --cov=."
.PHONY: test

clean: ## Clean repository
	find . -type f -name ".coverage" -exec rm -rf {} +
	find . -type d -name "dist" -exec rm -rf {} +
	find . -type d -name "build" -exec rm -rf {} +
	find . -type d -name "venv" -exec rm -rf {} +
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
.PHONY: clean

reset: ## Reset repository
	git clean -xdf || true
.PHONY: reset

help: ## Show help
	@grep -E '^[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
.PHONY: help

.EXPORT_ALL_VARIABLES:
DOCKER_BUILDKIT = 1
COMPOSE_DOCKER_CLI_BUILD = 1

.DEFAULT_GOAL := help
