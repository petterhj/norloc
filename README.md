# Development

## Backend

```sh
$ sudo apt install binutils libproj-dev gdal-bin postgresql-client-common
$ pip3 install pipenv
$ export PATH="$PATH:/home/user/.local/bin"
```

```sh
$ cd backend/
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install wheel
$ pip install -r requirements.txt

$ python manage.py makemigrations locations productions people
$ python manage.py migrate
$ python manage.py createsuperuser

$ python manage.py runserver
```

### Database

```sh
$ docker pull kartoza/postgis:13

$ docker run -d -t \
    --name "postgis" \
    -p 25432:5432 \
    -e POSTGRES_USER=postgres \
    -e POSTGRES_PASS=postgres \
    kartoza/postgis

$ apt install postgres-client-13

$ pg_isready -h localhost -p 25432 -U postgres

$ psql -h localhost -p 25432 -U postgres -f initdb.sql 
```

#### Backup and restore

```sh
$ pg_dump -h localhost -p 25432 -U postgres \
    --format=t \
    --file norloc_db.tar \
    --create \
    norloc

$ tar -xvf norloc_db.tar restore.sql # extract sql file

$ pg_restore -h localhost -p 25432 -U postgres \
    --dbname=norloc \
    norloc_db.tar
```


## Frontend

```sh
$ cd frontend/
$ npm install
$ npm run dev
```

Built using
* [Nuxt 3](https://v3.nuxtjs.org/)
* [Vue.js](https://vuejs.org/)
* [Windi CSS](https://windicss.org/)
* [Headless UI](https://headlessui.dev/)

### Resources

* https://www.kartverket.no/til-lands/stadnamn/sok-stadnamn-i-kart
* https://ws.geonorge.no/SKWS3Index/ssr/json/sok?navn=ny
* https://www.kartverket.no/api-og-data/stedsnavndata/brukarrettleiing-stadnamn-api
* https://objektkatalog.geonorge.no/Objekttype/Index/EAID_3E60BA7D_DDCD_43c0_B898_567F3167A37E
* https://objektkatalog.geonorge.no/Help/Api/GET-api-object-id
* https://objektkatalog.geonorge.no/api/object/EAID_3E60BA7D_DDCD_43c0_B898_567F3167A37E


# Deployment

## Database

### Setup

```sh
$ sudo apt update
$ sudo apt -y install postgresql postgresql-contrib postgis # Install PostgreSQL and PostGIS

$ sudo -u postgres createuser --interactive # Create role
Enter name of role to add: norloc
Shall the new role be a superuser? (y/n) n
Shall the new role be allowed to create databases? (y/n) y
Shall the new role be allowed to create more new roles? (y/n) n

$ sudo -u postgres createdb norloc # Create database
$ sudo -u postgres psql
```
```postgres
postgres=# \c norloc
norloc=# CREATE EXTENSION postgis; # Enable PostGIS
```
```sh
$ sudo adduser norloc
$ sudo -u norloc psql
```
```postgres
norloc=> \conninfo  --: Connection info
norloc=> \du        --: List roles
norloc=> \dt        --: List relations
```
```sh
$ sudo nano /etc/postgresql/9.1/main/pg_hba.conf # Ensure remote connection is disabled (default)
```

### Backend

```sh
$ sudo apt -y install libpython3.8 python3.8-venv
$ sudo apt -y install build-essential libpq-dev python-dev # Install dependencies for using PostgresSQL
$ sudo apt -y install nginx supervisor
$ pip install --user pipenv
```
```sh
$ cd apps/
$ git clone ....
$ cd norloc/backend/

$ pipenv install
$ pipenv install gunicorn
$ pipenv shell

$ python manage.py migrate
$ python manage.py collectstatic
$ python manage.py runserver 0.0.0.0:8000   # Test
```

#### Supervisor/Gunicorn
```sh
$ sudo systemctl enable supervisor
$ sudo systemctl start supervisor

$ mkdir /home/norloc/logs
$ touch /home/norloc/logs/gunicorn-error.log
```
`/home/norloc/bin/norloc_start`
```ini
#!/bin/bash

NAME="norloc"
DIR=/home/norloc/app/norloc/backend
USER=norloc
GROUP=norloc
WORKERS=3
BIND=unix:/home/norloc/app/norloc.sock
DJANGO_SETTINGS_MODULE=norloc.settings
DJANGO_WSGI_MODULE=norloc.wsgi
LOG_LEVEL=error

cd $DIR

export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DIR:$PYTHONPATH

exec /home/norloc/.local/bin/pipenv run gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $WORKERS \
  --user=$USER \
  --group=$GROUP \
  --bind=$BIND \
  --log-level=$LOG_LEVEL \
  --log-file=-
```
```sh
$ chmod u+x /home/norloc/bin/norloc_start
```

`/etc/supervisor/conf.d/norloc.conf`
```ini
[program:norloc]
command=/home/norloc/app/norloc/backend/bin/gunicorn
user=norloc
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/home/norloc/logs/gunicorn-error.log
```
```sh
$ sudo supervisorctl reread
$ sudo supervisorctl update
$ sudo supervisorctl status norloc
$ sudo supervisorctl restart norloc
```

#### nginx
```sh
upstream app_server {
    server unix:/home/norloc/app/norloc/run/gunicorn.sock fail_timeout=0;
}
server {
    location /static/ {
        alias /home/norloc/app/norloc/backend/static/;
    }
    location / {
        try_files $uri @proxy_to_app;
    }
    location @proxy_to_app {
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        proxy_pass http://app_server;
    }
}
```

#### Updating
```sh
$ cd apps/norloc/
$ pipenv shell
$ git pull origin master
$ pipenv install
$ python manage.py migrate
$ python manage.py collectstatic
$ sudo supervisorctl restart norloc
```

#### References

* https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-18-04
* https://simpleisbetterthancomplex.com/tutorial/2016/10/14/how-to-deploy-to-digital-ocean.html