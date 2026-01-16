.PHONY: up down backend frontend backend-attach frontend-attach build

up:
	docker-compose up -d

down:
	docker-compose down

backend:
	docker-compose exec backend bash

frontend:
	docker-compose exec frontend bash

backend-attach:
	make down
	make up
	make backend

frontend-attach:
	make down
	make up
	make frontend

build:
	docker-compose build
