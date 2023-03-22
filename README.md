# WIP:Django-Taberna

## For local development

1.Create a dev folder at the root of the project

```
./dev
```

2.In the './dev' folder, create a configuration file '.env.dev' and assign a value to the constants

```
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=django_taberna_dev
SQL_USER=django_user
SQL_PASSWORD=django_pass
SQL_HOST=db
SQL_PORT=5432
EMAIL_HOST=your_host
EMAIL_PORT=587
EMAIL_HOST_USER=your_email
EMAIL_HOST_PASSWORD=your_password
EMAIL_USE_TLS=1
```

2.In the './dev' folder, create a configuration file '.env.dev.db' and assign a value to the constants

```
POSTGRES_USER=django_user
POSTGRES_PASSWORD=django_pass
POSTGRES_DB=django_taberna_dev
```

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
nvm use 19.7.0
cd shop/apps/core/_dev
npm install
npm run w
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
