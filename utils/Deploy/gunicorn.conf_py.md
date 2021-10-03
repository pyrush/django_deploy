# for /etc/hitaisi/gunicorn.conf.py

# cd etc
# mkdir hitaisi
# cd hitaisi
# touch gunicorn.conf.py

workers = 3
syslog = True
bind = ["127.0.0.1:8000]
umask = 0
loglevel = "info"
user = "rampal"
group = "rampal"

