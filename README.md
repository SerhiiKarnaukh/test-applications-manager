# Django-Taberna

## Development

```
docker-compose build
docker-compose up
```

### Create SuperUser with Docker

```
docker exec -it tb_django python ./shop/manage.py createsuperuser
```

## Production

```
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up
```
