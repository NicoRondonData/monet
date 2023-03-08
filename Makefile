ifneq ("$(wildcard $(PATH_TO_FILE))","")
    .env ?= .env
	include $(.env)
endif
APP_NAME = monet

.PHONY: load-env
load-env:
	export $(shell sed 's/=.*//' $(.env))

.PHONY: help
help: ## Print help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_.-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

.PHONY: lint
lint:
	pre-commit run --all-files

.PHONY: test
test:
	./test.sh

.PHONY: build.linters
build.linters: ## Build a docker image for linters.
	docker build --pull --target linters -t $(APP_NAME)-linters .

.PHONY: lint.local
lint.local:
	docker-compose exec monet poetry run pre-commit run --all-files

.PHONY: lint.docker
lint.docker:
	docker run --rm --name $(APP_NAME)-linters $(APP_NAME)-linters:latest

.PHONY: test.local
test.local:
	docker-compose exec monet ./test.sh


.PHONY: build.dev
build.dev:
	docker-compose build

.PHONY: run.local
run.local:
	docker-compose up -d

.PHONY: rmi.linters
rmi.linters:
	docker rmi -f $(APP_NAME)-linters

.PHONY: rmi.test
rmi.tests:
	docker rmi -f $(APP_NAME)-test

.PHONY: clean
clean:
	docker-compose down -v
