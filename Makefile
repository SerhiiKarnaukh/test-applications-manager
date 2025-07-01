# Load variables from .env
include .env
export

run:
	docker-compose up -d

build:
	docker-compose up -d --build

test:
	docker-compose run --rm app sh -c "flake8"
	docker-compose run --rm app sh -c "coverage run manage.py test"
	docker-compose run --rm app sh -c "coverage report"
	docker-compose run --rm app sh -c "coverage html"
	docker-compose down

stop:
	@echo "💾 Creating a database backup..."
	docker-compose exec db pg_dump -U $(SQL_USER) $(SQL_DATABASE) > temp/db_backup.sql
	@echo "⛔ Stopping docker-compose..."
	docker-compose down

backup:
	@echo "💾 Start backup..."
	docker-compose up -d
	docker-compose exec db dropdb -U $(SQL_USER) $(SQL_DATABASE)
	docker-compose exec db createdb -U $(SQL_USER) $(SQL_DATABASE)
	docker-compose exec -T db psql -U $(SQL_USER) $(SQL_DATABASE) < temp/db_backup.sql

migrate:
	docker-compose run --rm app sh -c "python manage.py makemigrations"
	docker-compose run --rm app sh -c "python manage.py migrate"

super:
	docker-compose run --rm app sh -c "python manage.py createsuperuser"

clean:
	docker-compose down
	docker builder prune --all -f
