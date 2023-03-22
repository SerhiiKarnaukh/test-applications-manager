# WIP:Django-Taberna

## For local development

```
docker-compose build
docker-compose up
```

### Basic commands

```
docker-compose run --rm web sh -c "django-admin startproject projects_name"
docker-compose run --rm web sh -c "python manage.py startapp apps_name"
docker-compose run --rm web sh -c "python manage.py makemigrations"
docker-compose up
docker exec -it tb_django python manage.py migrate
docker exec -it tb_django python manage.py createsuperuser
docker-compose -f docker-compose.yml -f docker-compose-debug.yml up --build + F5
```

### Front-end

```
```

### For debugging

```
```

### Create your own project

```
```

## Production

```
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up
```
