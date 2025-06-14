DC = docker compose
API_CONTAINER = backend_api

.PHONY: up down bash
up:
	${DC} up

down:
	${DC} down

bash:
	@echo 'run -> docker compose exec -it backend_api bash'
	${DC} exec -it ${API_CONTAINER} bash
db_bash:
	@echo 'run -> docker compose exec -it local_database bash'
	${DC} exec -it ${DB_CONTAINER} bash
