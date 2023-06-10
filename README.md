# Exchange currency from API
## Introduction 

---
### Docker steps 
**1. Create network** 
```
docker network create exchange_network
```
**2. Build exchange_mysql container**
```
docker run -d --name exchange-mysql -p 3308:3306 -v "D:/Sources/exchange-rate/data:/var/lib/mysql" --network exchange_network --env-file .env  mysql
```
**3. Create Django project (one time)**
```
docker run -it --rm -v "D:/Sources/exchange-rate/src:/app" --network exchange_network python:3.7.1 bash -c "pip install django && django-admin startproject exchangerate && mv exchangerate/* /app/ && rmdir exchangerate"
```
**4. Build Image exchange**
```
docker build -t exchange .
```
**5. Create Exchange-web server**
```
docker run -it --rm -p 8000:8000 --name exchange_web -v "D:/Sources/exchange-rate/src:/app" --network exchange_network exchange
```
---
### Migrate database
1. Execute to container application 
> *docker exec -it exchange_web /bin/bash*

2. Run migrate in order to all default dbs's Django  (one time)
> *python manage.py migrate*

3. Get the last Django (ignore 'sessions')
> *SELECT * FROM <database_name>.django_migrations order by applied desc;*

4. Run makemigrations (make sure to have all Models) & add the last Django (3) into 'dependencies' 
> - *python manage.py makemigrations*
> - *Add dependencies = [('auth', '<last_django(3)>'),]*

5. Change new migrations (if any)

6. Run Migrate to update any new changes form Models (from migrations files at step 4)
> *python manage.py migrate*


