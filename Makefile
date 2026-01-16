.PHONY: up down bash reattach build

up:
	docker-compose up -d

down:
	docker-compose down

bash:
	docker-compose exec backend bash

reattach:
	make down
	make up
	make bash

build:
	docker-compose build
