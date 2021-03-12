# Analyze the given Python modules and compute Cyclomatic Complexity
cc_json = "$(shell radon cc --min D src --json)"
# Analyze the given Python modules and compute the Maintainability Index
mi_json = "$(shell radon mi --min B src --json)"

help: ## Display this help screen.
	@grep -h -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

lint: ## Run Pylint checks on the project.
	@pylint ./src

swagger_lint: ## Validate swagger documentation file
	@openapi-spec-validator ./src/swagger/openapi/openapi.json

fmt: ## Format all project files.
	@yapf src -r -i -vv

test: ## Run unit testings.
	@pytest -v

test-nocache: ## Run unit testing with out any cache
	@find . -name .pytest_cache -prune -exec rm -rf {} \;
	@pytest -v

install: ## Install project dependencies.
	@pip3 install --upgrade pip
	@pip3 install -r requirements-dev.txt
	@pip3 install -r requirements.txt

venv: ## Create new virtual environment. Run `source venv/bin/activate` after this command to enable it.
	@virtualenv venv --python=python3.8

run: ## Run local server.
	@python3 app.py

complexity: ## Run radon complexity checks for maintainability status.
	@echo "Complexity check..."

ifneq ($(cc_json), "{}")
	@echo
	@echo "Complexity issues"
	@echo "-----------------"
	@echo $(cc_json)
endif

ifneq ($(mi_json), "{}")
	@echo
	@echo "Maintainability issues"
	@echo "----------------------"
	@echo $(mi_json)
endif

ifneq ($(cc_json), "{}")
	@echo
	exit 1
else
ifneq ($(mi_json), "{}")
	@echo
	exit 1
endif
endif

	@echo "OK"
.PHONY: complexity