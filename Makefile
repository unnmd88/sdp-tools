APP_CONTAINER = fapiapp
EXEC = docker exec -it
TEST_IMAGE = fastapi-sdp-tools:tests
ACTIVATE_VENV = source .venv/bin/activate


#.PHONY: app
#up:
#	${DC} -f ${APP_FILE} ${ENV} up --build -d

.PHONY: activate 
activate:
	${ACTIVATE_VENV}	

.PHONY: up
up:
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

.PHONY: test
test:
	docker compose -f docker-compose.test.yml up --build -d
	docker compose -f docker-compose.test.yml exec -it test_app bash -c "pytest -vv -s"
	docker compose -f docker-compose.test.yml down --volumes
	docker rmi ${TEST_IMAGE}
