.PHONY: up down backend frontend backend-attach frontend-attach build \
	build-backend build-frontend up-backend down-backend up-frontend down-frontend

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

build-backend:
	docker-compose build backend

build-frontend:
	docker-compose build frontend

up-backend:
	docker-compose up -d backend

down-backend:
	docker-compose stop backend

up-frontend:
	docker-compose up -d frontend

down-frontend:
	docker-compose stop frontend
