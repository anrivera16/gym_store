start: ## Start the docker containers
	@echo "Starting the docker containers"
	@docker compose up
	@echo "Containers started - http://localhost:8000"

stop: ## Stop Containers
	@docker compose down

restart: stop start ## Restart Containers

start-bg:  ## Run containers in the background
	@docker compose up -d

build: ## Build Containers
	@docker compose build

ssh: ## SSH into running web container
	docker compose exec web bash

migrations: ## Create DB migrations in the container
	@docker compose exec web python manage.py makemigrations

migrate: ## Run DB migrations in the container
	@docker compose exec web python manage.py migrate

translations:
	@docker compose exec web python manage.py makemessages --all --ignore node_modules --ignore venv
	@docker compose exec web python manage.py makemessages -d djangojs --all --ignore node_modules --ignore venv
	@docker compose exec web python manage.py compilemessages

shell: ## Get a Django shell
	@docker compose exec web python manage.py shell

dbshell: ## Get a Database shell
	@docker compose exec db psql -U postgres gym_store

test: ## Run Django tests
	@docker compose exec web python manage.py test

init: start-bg migrations migrate bootstrap_content  ## Quickly get up and running (start containers and migrate DB)

pip-compile: ## Compiles your requirements.in file to requirements.txt
	@docker compose exec web pip-compile requirements/requirements.in
	@docker compose exec web pip-compile requirements/dev-requirements.in
	@docker compose exec web pip-compile requirements/prod-requirements.in

requirements: pip-compile build restart  ## Rebuild your requirements and restart your containers

black: ## Runs black on the codebase
	@docker compose exec web black --extend-exclude migrations --line-length 120 .

isort: ## Runs isort on the codebase
	@docker compose exec web isort -l 120 --profile black .

format: black isort ## Runs formatting (black and isort) on the codebase

npm-install: ## Runs npm install in the container
	@docker compose exec web npm install

npm-build: ## Runs npm build in the container (for production assets)
	@docker compose exec web npm run build

npm-dev: ## Runs npm dev in the container
	@docker compose exec web npm run dev

npm-watch: ## Runs npm watch in the container (recommended for dev)
	@docker compose exec web npm run dev-watch

npm-type-check: ## Runs the type checker on the front end TypeScript code
	@docker compose exec web npm run type-check

api-client:  ## Update the API client. See these notes for pointers: https://docs.saaspegasus.com/apis.html#generating-the-api-client
	@docker run --rm -v ${PWD}/assets/javascript/api-client:/local openapitools/openapi-generator-cli generate \
	-i http://${HOST_IP}:8000/api/schema/ \
	-g typescript-fetch \
	-o /local/

bootstrap_content:  ## Initializes your Wagtail content with some example pages and blog posts
	@docker compose exec web python manage.py bootstrap_content

upgrade: pip-compile build start-bg migrations migrate npm-install npm-dev

.PHONY: help
.DEFAULT_GOAL := help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
