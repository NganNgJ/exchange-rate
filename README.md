## Exchange currency from API

---
### Create network 
```
docker network create exchange_network
```

### Build exchange_mysql container
```
docker run -d --name exchange-mysql -p 3308:3306 -v "D:/Sources/exchange-rate/data:/var/lib/mysql" --network exchange_network --env-file .env  mysql
```

### Create Django project
```
docker run -it --rm -v "D:/Sources/exchange-rate/src:/app" --network exchange_network python:3.7.1 bash -c "pip install django && django-admin startproject exchangerate && mv exchangerate/* /app/ && rmdir exchangerate"
```

### Build Image exchange
```
docker build -t exchange .
```

### Create Web server
```
docker run -it --rm --network exchange_network -p 8000:8000 --name exchange_web -v "D:/Sources/exchange-rate/src:/app" exchange
```


