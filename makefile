test:
	docker-compose run --rm app sh -c "python manage.py wait_for_db && python manage.py test"

run:
	docker-compose up

build:
	docker-compose build