.ONESHELL:
SHELL = /bin/bash

GREEN := $(shell tput setaf 2)
YELLOW := $(shell tput setaf 3)
WHITE := $(shell tput setaf 7)
CYAN := $(shell tput setaf 6)
BOLD :=$(shell tput bold)

default: help

help: ## Show this help.
	@echo ''
	@echo 'Usage:'
	@echo '  ${YELLOW}make${RESET} ${GREEN}<target>${RESET}'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} { \
		if (/^[a-zA-Z_.-]+:.*?##.*$$/) {printf "    ${YELLOW}%-20s${GREEN}%s${RESET}\n", $$1, $$2} \
		else if (/^## .*$$/) {printf "  ${CYAN}%s${RESET}\n", substr($$1,4)} \
		}' $(MAKEFILE_LIST)

.PHONY: waypoint
waypoint: ## Builds and pushes a new docker image using Hashicorp waypoint
	waypoint init
	waypoint build

install_deps_app: ## Install dependencies required for application
	pip install -r requirements.txt

install_deps_dev: ## Install dependencies required for development
	pip install -r requirements-dev.txt

install_deps_all: install_deps_app install_deps_dev ## Install both application and development dependencies

compile_deps_app: ## Compile a new requirements.txt from requirements.in
	pip-compile requirements.in

compile_deps_dev: ## Compile a new requirements-dev.txt from requirements-dev.txt
	pip-compile requirements-dev.in

upgade_deps_app: ## Upgrade dependencies in requirements.txt
	pip-compile --upgrade requirements.in

upgrade_deps_dev: ## Upgrade dependencies in requirements-dev.txt
	pip-compile --upgrade requirements-dev.in

compile_deps_all: compile_deps_app compile_deps_dev ## Compile both application and development dependencies

lint: ## Lint code
	black src

lint_check: ## Check code linting
	black src --check

test_smoke_local: ## Run Bruno API collection test against local application
	bash -c 'cd ./tests/smoke/Webapi && bru run -r --env webapi-local'
test_smoke_docker: ## Run Bruno API collection test against dockerised application
	docker compose up --build --abort-on-container-exit --always-recreate-deps --force-recreate --exit-code-from test-smoke-local-docker test-smoke-local-docker

test_unit: ## Run unit tests
	python -m pytest ./tests/unit

start_local: ## Start local server
	python -m uvicorn src.delivery.http.main:app --port 8001 --reload --env-file .env

