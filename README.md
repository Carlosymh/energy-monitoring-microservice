# Energy Monitoring Microservice

Sistema de monitoreo continuo para plantas de generación de energía.

## Requisitos
- Python
- Docker
- docker-compose

## Instrucciones

# Construye y levanta los contenedores con docker-compose:
docker compose up -d django
docker compose build django
docker compose up django

# En otra terminal, ejecuta las migraciones de Django:
docker-compose exec django python manage.py migrate

# Accede a la documentación Swagger:

http://localhost:8000/docs/

# Para detener los servicios, puedes utilizar

docker composer down