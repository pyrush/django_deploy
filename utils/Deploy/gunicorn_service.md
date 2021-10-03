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

