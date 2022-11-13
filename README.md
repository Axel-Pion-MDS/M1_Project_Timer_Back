# MDS M1 - Project Timer Back
![Pythonlatest](https://img.shields.io/badge/Python-latest-%23316A9A)
![Django4.1.3](https://img.shields.io/badge/Django-v.4.1.3-%230C4B33)

## Packages
![Psycopg22.9.5](https://img.shields.io/badge/Psycogp2-v.2.9.5-%23009977)

## Getting started

## Before starting

Check if you have installed the following application :

- Docker

## How use application

### Create .env file

```bash
$ cp .env.sample .env
```

### Update variables inside .env file

```bash
$ touch .env
```

Modify the file with the value you want
```pycon
# Configure database name, user and password.
POSTGRES_DB=your_db_name
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password

# Database manager PGADMIN
PGADMIN_DEFAULT_EMAIL=your_email
PGADMIN_DEFAULT_PASSWORD=your_password
```

### Build application

```bash
$ docker-compose build
```

### Start application

```bash
$ docker-compose up -d
```

### Migrate the database

```bash
$ docker-compose run --rm api python manage.py makemigrations
$ docker-compose run --rm api python manage.py migrate
```

Use -d if you want to detach the container

## Postman

