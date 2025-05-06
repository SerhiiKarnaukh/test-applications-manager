# Test Applications Manager

### App on AWS: <https://django.karnaukh-webdev.com/>

![TAM screenshot](https://github.com/SerhiiKarnaukh/test-applications-manager/blob/main/tam.jpg)

## For local development

```
docker-compose build
docker-compose run --rm app sh -c "python manage.py makemigrations"
docker-compose run --rm app sh -c "python manage.py migrate"
docker-compose run --rm app sh -c "python manage.py createsuperuser"
docker-compose up -d --build
```

### Front-end Store

```
nvm use 22.15.0
cd portfolio/apps/taberna_product/_dev
npm install
npm run w
```

### Front-end Core

```
nvm use 22.15.0
cd portfolio/apps/core/_dev
npm install
npm run w
```

### Test

1. Create report

```
docker-compose run --rm app sh -c "coverage run manage.py test"
docker-compose run --rm app sh -c "coverage report"
docker-compose run --rm app sh -c "coverage html"
```

2. Run Lint and Test

```
docker-compose run --rm app sh -c "flake8"
docker-compose run --rm app sh -c "python manage.py test"

docker-compose up
docker exec -it portfolio coverage run manage.py test
```
