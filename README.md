# WIP:Django Portfolio for Test Applications

## For local development

1. In the './dev' folder, create a configuration file '.env.dev.db' and '.env.dev' and assign a value to the constants

2. Build the image and make migrations

```
docker-compose build
docker-compose run --rm app sh -c "python manage.py makemigrations"
docker-compose run --rm app sh -c "python manage.py migrate"
docker-compose run --rm app sh -c "python manage.py createsuperuser"
```

3. Run container

```
docker-compose up
```

4. Go to admin panel and add test content

```
http://127.0.0.1:8000/admin
```

### Front-end Store

```
nvm use 19.7.0
cd portfolio/apps/product/_dev
npm install
npm run w
```

### For debugging

```
1.See .vscode/launch.json
2.docker-compose -f docker-compose.yml -f docker-compose-debug.yml up --build + F5
```

### Tests

1. Create report

```
docker-compose run --rm app sh -c "coverage run manage.py test"
docker-compose run --rm app sh -c "coverage report"
docker-compose run --rm app sh -c "coverage html"
```

2. Run Tests

```
docker-compose up
docker exec -it portfolio coverage run manage.py test
```

### Create your own project with this Dockerfile

```
1.Create your dependency file 'req.txt' (Django + psycopg2)
2.Create .dockerignore
3.Commands:
docker-compose build
docker-compose run --rm app sh -c "django-admin startproject projects_name"
4.Change the 'settings.py' file to take into account the database connection constants
5.Next commands:
docker-compose run --rm app sh -c "python manage.py startapp apps_name"
docker-compose run --rm app sh -c "python manage.py makemigrations"
docker-compose run --rm app sh -c "python manage.py migrate"
docker-compose run --rm app sh -c "python manage.py createsuperuser"
```

## Production test for deploy

```
docker-compose -f docker-compose-deploy.yml down --volumes
docker-compose -f docker-compose-deploy.yml build
docker-compose -f docker-compose-deploy.yml up
docker-compose -f docker-compose-deploy.yml run --rm app sh -c "python manage.py createsuperuser"
```
