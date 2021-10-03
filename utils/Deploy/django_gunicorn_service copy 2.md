# for /etc/systemd/system/gunicorn.service

[Unit]
Description=hitaisi

[Service]
Type=simple
PIDFile=/home/data/Hitaisi/WebApp/gunicorn.pid
User=rampal
Group=rampal
WorkingDirectory=/home/data/Hitaisi/WebApp
ExecStart=/home/data/Hitaisi/WebApp/venv/bin/gunicorn \
          --config /etc/hitaisi/gunicorn.conf.py \
          hitaisi.wsgi:application


ExecReload=/bin/kill -s HUP $MAINPID
ExecStop=/bin/kill -s TERM $MAINPID

[Install]
WantedBy=multi-user.target


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


* /etc/nginx/sites-available/myproject

* server {
    listen 80;
    server_name server_domain_or_IP;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/data/Hitaisi/WebApp;
    }
    location /media/ {
        root /home/data/Hitaisi/WebApp;
    }

    location / {
        include proxy_params;
        proxy_pass http://localhost:8000;
    }
}
* 


