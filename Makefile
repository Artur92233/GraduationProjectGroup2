DC = docker compose

.PHONY: up down
up:
	${DC} up


down:
	${DC} down