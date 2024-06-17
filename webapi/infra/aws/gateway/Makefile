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

prepare: ## Selects terraform version and initialises its modules.
	tfswitch
	terraform init
	terraform workspace select uat

apply: prepare ## Applies the terraform module.
	terraform apply -var-file vars/uat/common.tfvars -auto-approve

deploy: apply ## Applies terraform and deploy the changes to the API Gateway.
	$(eval AWS_REGION := $(shell terraform output -json | jq -r .aws_region.value))

destroy: prepare ## Destroys the AWS resources (Clean up).
	terraform destroy -var-file vars/uat/common.tfvars # -auto-approve

complete:  deploy destroy ## Deploys the project and Cleans the resources automatically.
	@echo "Build and Clean Module for Testing"
