APP_CONTAINER = fapiapp
TEST_APP_CONTAINER = test_app
EXEC = docker exec -it
TEST_IMAGE = fastapi-sdp-tools:tests
ACTIVATE_VENV = source .venv/bin/activate


#.PHONY: app
#up:
#	${DC} -f ${APP_FILE} ${ENV} up --build -d

.PHONY: activate 
activate:
	${ACTIVATE_VENV}	

lint: ## Run linting with ruff
	uv run ruff check app/

format: ## Format code with ruff
	uv run ruff format app/

.PHONY: up
up:
	docker compose up

.PHONY: upd
upd:
	docker compose up -d

.PHONY: up-build
up-build:
	docker compose up --build -d

.PHONY: down
down:
	docker compose down --volumes

.PHONY: upgrade
upgrade:
	alembic upgrade head


.PHONY: app-shell
app-shell:
	${EXEC} ${APP_CONTAINER} bash

.PHONY: tst
tst:
	uv run pytest tests/

.PHONY: tst-v
tst-v:
	uv run pytest tests/ -vv -s

test-cov: ## Run tests with coverage
	uv run pytest tests/ -v --cov=app --cov-report=html --cov-report=term

.PHONY: test
test:
	docker compose -f docker-compose.test.yml up --build -d
	docker compose -f docker-compose.test.yml exec -it ${TEST_APP_CONTAINER} bash -c  \
	"ls -a;cd ..;source .venv/bin/activate;ls -a;uv run pytest tests/ -vv -s"
	#" which python; cd app;ls -a;uv run pytest tests/ -vv -s"

	docker compose -f docker-compose.test.yml down --volumes
	docker rmi ${TEST_IMAGE}

.PHONY: test-down
test-down:
	docker compose -f docker-compose.test.yml down --volumes
	docker rmi ${TEST_IMAGE}