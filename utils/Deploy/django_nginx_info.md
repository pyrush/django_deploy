* For Django with Python 3

# sudo apt update
# sudo apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx curl

* Postgres
# sudo -u postgres psql
# CREATE DATABASE myproject;
# CREATE USER myprojectuser WITH PASSWORD 'password';

# ALTER ROLE myprojectuser SET client_encoding TO 'utf8';
# ALTER ROLE myprojectuser SET default_transaction_isolation TO 'read committed';
# ALTER ROLE myprojectuser SET timezone TO 'UTC';

# GRANT ALL PRIVILEGES ON DATABASE myproject TO myprojectuser;
# \q
# exit


* Creating a Python Virtual Environment for your Project

# sudo -H pip3 install --upgrade pip
# sudo -H pip3 install virtualenv

# mkdir ~/myprojectdir
# cd ~/myprojectdir

# virtualenv myprojectenv
# source myprojectenv/bin/activate

* Creating and Configuring a New Django Project

# pip install django gunicorn psycopg2-binary

# django-admin.py startproject myproject ~/myprojectdir

# nano ~/myprojectdir/myproject/settings.py

. . .
# The simplest case: just add the domain name(s) and IP addresses of your Django server
# ALLOWED_HOSTS = [ 'example.com', '203.0.113.5']
# To respond to 'example.com' and any subdomains, start the domain with a dot
# ALLOWED_HOSTS = ['.example.com', '203.0.113.5']
ALLOWED_HOSTS = ['your_server_domain_or_IP', 'second_domain_or_IP', . . ., 'localhost']

# #############################################

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'myproject',
        'USER': 'myprojectuser',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '',
    }
}

# ############################################


STATIC_URL = '/static/'
import os
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

~/myprojectdir/manage.py makemigrations
~/myprojectdir/manage.py migrate
 
* Create an administrative user for the project by typing:

~/myprojectdir/manage.py createsuperuser

~/myprojectdir/manage.py collectstatic

* Testing Gunicorn’s Ability to Serve the Project
The last thing we want to do before leaving our virtual environment is test Gunicorn to make sure that it can serve the application. We can do this by entering our project directory and using gunicorn to load the project’s WSGI module:

# cd ~/myprojectdir
# gunicorn --bind 0.0.0.0:8000 myproject.wsgi

# deactivate

* Creating systemd Socket and Service Files for Gunicorn

# sudo nano /etc/systemd/system/gunicorn.socket

[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target

# sudo nano /etc/systemd/system/gunicorn.service

[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=sammy
Group=www-data
WorkingDirectory=/home/sammy/myprojectdir
ExecStart=/home/sammy/myprojectdir/myprojectenv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          myproject.wsgi:application

[Install]
WantedBy=multi-user.target


# sudo systemctl start gunicorn.socket
# sudo systemctl enable gunicorn.socket

* gunicorn socket file
# sudo systemctl status gunicorn.socket


* Next, check for the existence of the gunicorn.sock file within the /run directory:

# file /run/gunicorn.sock

Output
/run/gunicorn.sock: socket

# sudo journalctl -u gunicorn.socket

* Testing Socket Activation
Currently, if you’ve only started the gunicorn.socket unit, the gunicorn.service will not be active yet since the socket has not yet received any connections. You can check this by typing:

sudo systemctl status gunicorn
 
Output
● gunicorn.service - gunicorn daemon
   Loaded: loaded (/etc/systemd/system/gunicorn.service; disabled; vendor preset: enabled)
   Active: inactive (dead)

* To test the socket activation mechanism, we can send a connection to the socket through curl by typing:
# curl --unix-socket /run/gunicorn.sock localhost

* You should see the HTML output from your application in the terminal. This indicates that Gunicorn was started and was able to serve your Django application. You can verify that the Gunicorn service is running by typing:

# sudo systemctl status gunicorn
 
Output
● gunicorn.service - gunicorn daemon
   Loaded: loaded (/etc/systemd/system/gunicorn.service; disabled; vendor preset: enabled)
   Active: active (running) since Mon 2018-07-09 20:00:40 UTC; 4s ago
 Main PID: 1157 (gunicorn)
    Tasks: 4 (limit: 1153)
   CGroup: /system.slice/gunicorn.service
           ├─1157 /home/sammy/myprojectdir/myprojectenv/bin/python3 /home/sammy/myprojectdir/myprojectenv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/run/gunicorn.sock myproject.wsgi:application
           ├─1178 /home/sammy/myprojectdir/myprojectenv/bin/python3 /home/sammy/myprojectdir/myprojectenv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/run/gunicorn.sock myproject.wsgi:application
           ├─1180 /home/sammy/myprojectdir/myprojectenv/bin/python3 /home/sammy/myprojectdir/myprojectenv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/run/gunicorn.sock myproject.wsgi:application
           └─1181 /home/sammy/myprojectdir/myprojectenv/bin/python3 /home/sammy/myprojectdir/myprojectenv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/run/gunicorn.sock myproject.wsgi:application

Jul 09 20:00:40 django1 systemd[1]: Started gunicorn daemon.
Jul 09 20:00:40 django1 gunicorn[1157]: [2018-07-09 20:00:40 +0000] [1157] [INFO] Starting gunicorn 19.9.0
Jul 09 20:00:40 django1 gunicorn[1157]: [2018-07-09 20:00:40 +0000] [1157] [INFO] Listening at: unix:/run/gunicorn.sock (1157)
Jul 09 20:00:40 django1 gunicorn[1157]: [2018-07-09 20:00:40 +0000] [1157] [INFO] Using worker: sync
Jul 09 20:00:40 django1 gunicorn[1157]: [2018-07-09 20:00:40 +0000] [1178] [INFO] Booting worker with pid: 1178
Jul 09 20:00:40 django1 gunicorn[1157]: [2018-07-09 20:00:40 +0000] [1180] [INFO] Booting worker with pid: 1180
Jul 09 20:00:40 django1 gunicorn[1157]: [2018-07-09 20:00:40 +0000] [1181] [INFO] Booting worker with pid: 1181
Jul 09 20:00:41 django1 gunicorn[1157]:  - - [09/Jul/2018:20:00:41 +0000] "GET / HTTP/1.1" 200 163

# sudo journalctl -u gunicorn

* Check your /etc/systemd/system/gunicorn.service file for problems. If you make changes to the /etc/systemd/system/gunicorn.service file, reload the daemon to reread the service definition and restart the Gunicorn process by typing:

sudo systemctl daemon-reload
sudo systemctl restart gunicorn
# #####################################################

* Configure Nginx to Proxy Pass to Gunicorn
Now that Gunicorn is set up, we need to configure Nginx to pass traffic to the process.

Start by creating and opening a new server block in Nginx’s sites-available directory:

# sudo nano /etc/nginx/sites-available/myproject


* /etc/nginx/sites-available/myproject

* server {
    listen 80;
    server_name server_domain_or_IP;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/sammy/myprojectdir;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
* 

* cresate symlink to sites-enabled
# sudo ln -s /etc/nginx/sites-available/myproject /etc/nginx/sites-enabled

# sudo nginx -t

# sudo systemctl restart nginx



# #####################################################
>>>>>>>>>>>>>>> Troubleshoot
# #####################################################


Troubleshooting Nginx and Gunicorn
If this last step does not show your application, you will need to troubleshoot your installation.

Nginx Is Showing the Default Page Instead of the Django Application
If Nginx displays the default page instead of proxying to your application, it usually means that you need to adjust the server_name within the /etc/nginx/sites-available/myproject file to point to your server’s IP address or domain name.

Nginx uses the server_name to determine which server block to use to respond to requests. If you are seeing the default Nginx page, it is a sign that Nginx wasn’t able to match the request to a sever block explicitly, so it’s falling back on the default block defined in /etc/nginx/sites-available/default.

The server_name in your project’s server block must be more specific than the one in the default server block to be selected.

* Nginx Is Displaying a 502 Bad Gateway Error Instead of the Django Application
A 502 error indicates that Nginx is unable to successfully proxy the request. A wide range of configuration problems express themselves with a 502 error, so more information is required to troubleshoot properly.

The primary place to look for more information is in Nginx’s error logs. Generally, this will tell you what conditions caused problems during the proxying event. Follow the Nginx error logs by typing:

sudo tail -F /var/log/nginx/error.log
 
Now, make another request in your browser to generate a fresh error (try refreshing the page). You should see a fresh error message written to the log. If you look at the message, it should help you narrow down the problem.

# You might see some of the following message:

connect() to unix:/run/gunicorn.sock failed (2: No such file or directory)

# This indicates that Nginx was unable to find the gunicorn.sock file at the given location. You should compare the proxy_pass location defined within /etc/nginx/sites-available/myproject file to the actual location of the gunicorn.sock file generated by the gunicorn.socket systemd unit.

If you cannot find a gunicorn.sock file within the /run directory, it generally means that the systemd socket file was unable to create it. Go back to the section on checking for the Gunicorn socket file to step through the troubleshooting steps for Gunicorn.

# ###########################################################

# connect() to unix:/run/gunicorn.sock failed (13: Permission denied)

This indicates that Nginx was unable to connect to the Gunicorn socket because of permissions problems. This can happen when the procedure is followed using the root user instead of a sudo user. While systemd is able to create the Gunicorn socket file, Nginx is unable to access it.

This can happen if there are limited permissions at any point between the root directory (/) the gunicorn.sock file. We can see the permissions and ownership values of the socket file and each of its parent directories by passing the absolute path to our socket file to the namei command:

# namei -l /run/gunicorn.sock

Output
f: /run/gunicorn.sock
drwxr-xr-x root root /
drwxr-xr-x root root run
srw-rw-rw- root root gunicorn.sock

# The output displays the permissions of each of the directory components. By looking at the permissions (first column), owner (second column) and group owner (third column), we can figure out what type of access is allowed to the socket file.

In the above example, the socket file and each of the directories leading up to the socket file have world read and execute permissions (the permissions column for the directories end with r-x instead of ---). The Nginx process should be able to access the socket successfully.

If any of the directories leading up to the socket do not have world read and execute permission, Nginx will not be able to access the socket without allowing world read and execute permissions or making sure group ownership is given to a group that Nginx is a part of.

# Django Is Displaying: “could not connect to server: Connection refused”
One message that you may see from Django when attempting to access parts of the application in the web browser is:

OperationalError at /admin/login/
could not connect to server: Connection refused
    Is the server running on host "localhost" (127.0.0.1) and accepting
    TCP/IP connections on port 5432?

# This indicates that Django is unable to connect to the Postgres database. Make sure that the Postgres instance is running by typing:

sudo systemctl status postgresql
 
If it is not, you can start it and enable it to start automatically at boot (if it is not already configured to do so) by typing:

# sudo systemctl start postgresql
# sudo systemctl enable postgresql

# If you are still having issues, make sure the database settings defined in the ~/myprojectdir/myproject/settings.py file are correct.


Further Troubleshooting
For additional troubleshooting, the logs can help narrow down root causes. Check each of them in turn and look for messages indicating problem areas.

The following logs may be helpful:

Check the Nginx process logs by typing: sudo journalctl -u nginx
Check the Nginx access logs by typing: sudo less /var/log/nginx/access.log
Check the Nginx error logs by typing: sudo less /var/log/nginx/error.log
Check the Gunicorn application logs by typing: sudo journalctl -u gunicorn
Check the Gunicorn socket logs by typing: sudo journalctl -u gunicorn.socket


# As you update your configuration or application, you will likely need to restart the processes to adjust to your changes.

If you update your Django application, you can restart the Gunicorn process to pick up the changes by typing:

# sudo systemctl restart gunicorn

If you change Gunicorn socket or service files, reload the daemon and restart the process by typing:

# sudo systemctl daemon-reload
# sudo systemctl restart gunicorn.socket gunicorn.service

* If you change the Nginx server block configuration, test the configuration and then Nginx by typing:

# sudo nginx -t && sudo systemctl restart nginx


