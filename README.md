# WIP:Django-Taberna

## For local development

1. In the './dev' folder, create a configuration file '.env.dev.db' and '.env.dev' and assign a value to the constants

2. Build the image and make migrations

```
docker-compose build
docker-compose run --rm web sh -c "python manage.py makemigrations"
```

3. Create container and migrate database migrations and also create superuser

```
docker-compose up
docker exec -it tb_django python manage.py migrate
docker exec -it tb_django python manage.py createsuperuser
```

4. Go to admin panel and add test content

```
http://127.0.0.1:8000/admin
```

### Front-end

```
nvm use 19.7.0
cd shop/apps/core/_dev
npm install
npm run w
```

### For debugging

```
docker-compose -f docker-compose.yml -f docker-compose-debug.yml up --build + F5
```

### Create your own project

```
docker-compose run --rm web sh -c "django-admin startproject projects_name"
docker-compose run --rm web sh -c "python manage.py startapp apps_name"
```

## Production

```
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up
```
