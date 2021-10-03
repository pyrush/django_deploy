# /etc/nginx/sites-available/myproject

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


