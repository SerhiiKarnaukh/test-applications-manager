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

for test trends:
docker-compose run --rm app sh -c "python portfolio/apps/scripts/generate_trends.py"
```

### Front-end Store

```
nvm use 20.14.0
cd portfolio/apps/product/_dev
npm install
npm run w
```

### Front-end Core

```
nvm use 20.14.0
cd portfolio/apps/core/_dev
npm install
npm run w
```

### For debugging

```
1.See .vscode/launch.json
2.docker-compose -f docker-compose.yml -f docker-compose-debug.yml up --build + F5
```

### Test

1. Create report

```
docker-compose run --rm app sh -c "coverage run manage.py test"
docker-compose run --rm app sh -c "coverage report"
docker-compose run --rm app sh -c "coverage html"
```

2. Run Test

```
docker-compose up
docker exec -it portfolio coverage run manage.py test
```
