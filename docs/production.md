### source: https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-22-04
### installing nginx on Ubuntu 22.04: https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-ubuntu-22-04

### How To Set Up Let's Encrypt with Nginx Server Blocks on Ubuntu 16.04: https://www.digitalocean.com/community/tutorials/how-to-set-up-let-s-encrypt-with-nginx-server-blocks-on-ubuntu-16-04

### Install and Secure Redis on Ubuntu 22.04: https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-redis-on-ubuntu-22-04



#create migrations
`python3 manage.py makemigrations`

#apply migrations to db
`python3 manage.py migrate`

#create supseruser
`python3 manage.py createsuperuser`

#collect static files
`python3 manage.py collectstatic`


######

    If you followed the initial server setup guide, 
    you should have a UFW firewall protecting your server. 
    In order to test the development server, you need 
    to allow access to the port you’ll be using.


Create an exception for port 8000:
`sudo ufw allow 8000`

test out project by starting up the Django development server:
`python3 manage.py runserver 0.0.0.0:8000`

In web browser, visit server’s domain name or IP address followed by :8000:
`http://server_domain_or_IP:8000`


if everything is ok, CTRL-C in the terminal window to shut down the development server.



#### Testing Gunicorn’s Ability to Serve the Project

`gunicorn --bind 0.0.0.0:8000 config.wsgi`

after testing CTRL-C in the terminal window to stop Gunicorn



#### Creating systemd Socket and Service Files for Gunicorn


The Gunicorn socket will be created at boot and will listen for connections. 
When a connection occurs, systemd will automatically start the Gunicorn 
process to handle the connection.


`sudo nano /etc/systemd/system/tinder.socket`

Inside, you will create 
[Unit] section to describe the socket, 
[Socket] section to define the socket location, and 
[Install] section to make sure the socket is created at the right time:

## /etc/systemd/system/tinder.socket
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/tinder.sock

[Install]
WantedBy=sockets.target
##

save and close `tinder.socket` file


Next, create and open a systemd service file for Gunicorn with sudo 
privileges in your text editor. The service filename should match 
the socket filename with the exception of the extension:

`sudo nano /etc/systemd/system/tinder.service`

[Unit] section, which is used to specify metadata and dependencies. 
Put a description of the service here and tell the init system to only start this 
after the networking target has been reached. Because your service relies on the 
socket from the socket file, you need to include a Requires directive to indicate 
that relationship:
[Service] section, specify the user and group that you want to process to run under. 
You will give your regular user account ownership of the process since it owns all 
of the relevant files. You’ll give group ownership to the www-data group so that 
Nginx can communicate easily with Gunicorn.
Then you’ll map out the working directory and specify the command to use to start 
the service. In this case, you have to specify the full path to the Gunicorn executable, 
which is installed within our virtual environment. You will then bind the process to 
the Unix socket you created within the /run directory so that the process can 
communicate with Nginx. You log all data to standard output so that the journald 
process can collect the Gunicorn logs. You can also specify any optional Gunicorn 
tweaks here. For example, you specified 3 worker processes in this case:
[Install] section, this will tell systemd what to link this service to if you 
enable it to start at boot. You want this service to start when the regular 
multi-user system is up and running:


## /etc/systemd/system/tinder.service
[Unit]
Description=gunicorn daemon
Requires=tinder.socket
After=network.target

[Service]
User=abror
Group=www-data
WorkingDirectory=/home/abror/tinder.uz
ExecStart=/home/abror/tinder.uz/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/tinder.sock \
          config.wsgi:application

[Install]
WantedBy=multi-user.target
##

Save and close.


You can now start and enable the Gunicorn socket. This will create the socket file 
at `/run/tinder.sock` now and at boot. When a connection is made to that socket, 
systemd will automatically start the gunicorn.service to handle it:


`sudo systemctl start tinder.socket`
`sudo systemctl enable tinder.socket`



#### Checking for the Gunicorn Socket File

Check the status of the process to find out whether it was able to start:

`sudo systemctl status tinder.socket`

Next, check for the existence of the gunicorn.sock file within the /run directory:

`file /run/tinder.sock`

Output:
/run/tinder.sock: socket

If the systemctl status command indicated that an error occurred or if you 
do not find the gunicorn.sock file in the directory, it’s an indication that 
the Gunicorn socket was not able to be created correctly. Check the Gunicorn 
socket’s logs by typing:

`sudo journalctl -u tinder.socket`



#### Testing Socket Activation

Currently, if you’ve only started the gunicorn.socket unit, the 
gunicorn.service will not be active yet since the socket has not 
yet received any connections. You can check this by typing:


`sudo systemctl status tinder`


To test the socket activation mechanism, you can send a connection 
to the socket through curl by typing:

`curl --unix-socket /run/tinder.sock localhost`

You should receive the HTML output from your application in the terminal. 
This indicates that Gunicorn was started and was able to serve your Django 
application. You can verify that the Gunicorn service is running by typing:

`sudo systemctl status tinder`


If the output from curl or the output of systemctl status indicates that a 
problem occurred, check the logs for additional details:

`sudo journalctl -u tinder`

Check your `/etc/systemd/system/tinder.service` file for problems. 
If you make changes to the `/etc/systemd/system/tinder.service` file, 
reload the daemon to reread the service definition and restart the 
Gunicorn process by typing:

`sudo systemctl daemon-reload`
`sudo systemctl restart tinder`



#### Configure Nginx to Proxy Pass to Gunicorn


Now that Gunicorn is set up, you need to configure Nginx to pass traffic to the process.
Start by creating and opening a new server block in Nginx’s sites-available directory:

`sudo nano /etc/nginx/sites-available/tinder`

open up a new server block. You will start by specifying that this block should listen 
on the normal port 80 and that it should respond to your server’s domain name or IP address:

Next, you will tell Nginx to ignore any problems with finding a favicon. You will also tell 
it where to find the static assets that you collected in your ~/myprojectdir/static directory. 
All of these files have a standard URI prefix of “/static”, so you can create a location 
block to match those requests:

Finally, create a location / {} block to match all other requests. Inside of this location, 
you’ll include the standard proxy_params file included with the Nginx installation and then 
pass the traffic directly to the Gunicorn socket:

##  /etc/nginx/sites-available/tinder
server {
    listen 80;
    server_name tinder-backend.elearn.uz;
    client_max_body_size 100M;

    location = /favicon.ico { access_log off; log_not_found off; }


    location /static/ {
        alias /home/abror/tinder.uz/static_root/;
    }
    location /media/ {
        alias /home/abror/tinder.uz/media_root/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/tinder.sock;
    }
}
##

Save and close

Now, you can enable the file by linking it to the sites-enabled/saylov_uchastkalari directory

`sudo ln -s /etc/nginx/sites-available/tinder /etc/nginx/sites-enabled/tinder`


Test your Nginx configuration for syntax errors by typing:

`sudo nginx -t`


If no errors are reported, go ahead and restart Nginx by typing:

`sudo systemctl restart nginx`


Finally, you need to open up your firewall to normal traffic on port 80. 
Since you no longer need access to the development server, you can remove 
the rule to open port 8000 as well:

`sudo ufw delete allow 8000`
`sudo ufw allow 'Nginx Full'`


#### if `sudo ufw allow 'Nginx Full'` command raises an error than enable 'Nginx Full'

You can see which apps are available by running this command:

`sudo ufw app list`

Ports: HTTP - 80 HTTPS - 443

Simple way to add them to UFW:

`sudo ufw allow 80,443/tcp`

If you are wanting to accomplish this via application you will need to create the application ini file within /etc/ufw/applications.d

Example:

`sudo nano /etc/ufw/applications.d/nginx.ini`

Place this inside file

##
[Nginx HTTP]
title=Web Server 
description=Enable NGINX HTTP traffic
ports=80/tcp

[Nginx HTTPS] \
title=Web Server (HTTPS) \
description=Enable NGINX HTTPS traffic
ports=443/tcp

[Nginx Full]
title=Web Server (HTTP,HTTPS)
description=Enable NGINX HTTP and HTTPS traffic
ports=80,443/tcp
##

Then type this commands

`sudo ufw app update nginx`

`sudo ufw app info 'Nginx HTTP'`

`sudo ufw allow 'Nginx HTTP'` 

`sudo ufw allow 'Nginx Full'`


You should now be able to go to your server’s domain or IP address to view your application.
