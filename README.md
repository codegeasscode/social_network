# Project Setup and Access Guide

This guide will walk you through setting up the project locally .Please follow these steps carefully for a smooth setup.

## Local Setup

1. Clone the project repository to your local machine.
2. Go inside social_network folder
3. run docker:
```
bash
sudo docker compose up -d
sudo docker compose up --build 
```
4. migrate:
```
bash
sudo docker compose exec web python manage.py migrate
```
5. check migration status
```
bash
sudo docker compose exec web python manage.py showmigrations
```
6. create superuser (optional)
- To access admin
http://localhost:8000/admin/
```
bash
sudo docker compose exec web python manage.py createsuperuser
```

### Prerequisites

- Docker must be installed on your machine.

### Postman collection

- under social_network folder
