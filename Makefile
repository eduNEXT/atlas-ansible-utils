.PHONY: requirements
help: ## Display this help message.
	@echo "Please use \`make <target>' where <target> is one of"
	@awk -F ':.*?## ' '/^[a-zA-Z]/ && NF==2 {printf "\033[36m  %-28s\033[0m %s\n", $$1, $$2}' Makefile | sort
piptools: ## install pinned version of pip-compile and pip-sync
	pip install -r requirements/pip-tools.txt

requirements: ## install  environment requirements
	pip install -r requirements/base.txt
	ansible-galaxy install -r requirements.yml

dev-requirements: ## install development requirements
	pip install -r requirements/dev.txt
	ansible-galaxy install -r requirements.yml

quality: ## Lint based in ansible.
	ansible-lint -c .ansible-lint.yml

format:
	ansible-lint -c .ansible-lint.yml --fix

upgrade: export CUSTOM_COMPILE_COMMAND=make upgrade
upgrade: piptools ## Upgrade requirements with pip-tools.
	pip-compile --upgrade requirements/pip-tools.in
	pip-compile --upgrade requirements/base.in
	pip-compile --upgrade requirements/dev.in

