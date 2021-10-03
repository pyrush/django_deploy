* Postgres
# sudo apt update
# sudo apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx curl


# sudo -u postgres psql
# CREATE DATABASE myproject;
# CREATE USER myprojectuser WITH PASSWORD 'password';

# ALTER ROLE myprojectuser SET client_encoding TO 'utf8';
# ALTER ROLE myprojectuser SET default_transaction_isolation TO 'read committed';
# ALTER ROLE myprojectuser SET timezone TO 'UTC';

# GRANT ALL PRIVILEGES ON DATABASE myproject TO myprojectuser;
# \q
# exit


# pip3 install dj-database-url
https://github.com/kennethreitz/dj-database-url

* Update database configuration from $DATABASE_URL.
* In /settings.py

# import dj_database_url
# DATABASES['default'] = dj_database_url.config(conn_max_age=600)
* Provide a default:
# DATABASES['default'] = dj_database_url.config(default='postgres://...')
* Parse an arbitrary Database URL:

# DATABASES['default'] = dj_database_url.parse('postgres://...', conn_max_age=600)

* or
# db_from_env = dj_database_url.config(conn_max_age=500)
# DATABASES['default'].update(db_from_env)

* URL schema
Engine - PostgreSQL
Django Backend - django.db.backends.postgresql
URL - postgres://USER:PASSWORD@HOST:PORT/NAME [


