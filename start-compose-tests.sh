#!/usr/bin/env bash


docker compose -f docker-compose.test.yml up --build -d
docker compose -f docker-compose.test.yml exec -it test_app bash -c "pytest -vv"
docker compose -f docker-compose.test.yml down --volumes
#docker rmi $(docker images --filter "dangling=true" -q --no-trunc)
docker rmi fastapi-sdp-tools:tests
