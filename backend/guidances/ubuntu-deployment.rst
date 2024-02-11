#|==============================================================================
#|          D E P L O Y M E N T   G U I D A N C E with Ubuntu 22.04
#|==============================================================================

1.1. INSTALL DATABASE POSTGRES 
--------------------------------------------------------------------------------
sudo apt update
sudo apt install postgresql postgresql-contrib

sudo -u postgres psql -c "CREATE USER uflaskvuepf WITH ENCRYPTED PASSWORD 'PwDflaskvuepfSatu1Dua3';"
sudo -u postgres psql -c "CREATE DATABASE db_flaskvuepf;"


sudo -u postgres psql db_flaskvuepf -c "GRANT ALL PRIVILEGES ON DATABASE db_flaskvuepf TO uflaskvuepf;"
sudo -u postgres psql db_flaskvuepf -c "GRANT ALL ON SCHEMA public TO uflaskvuepf;"
sudo -u postgres psql db_flaskvuepf -c "GRANT ALL ON ALL TABLES IN SCHEMA public to uflaskvuepf;"
sudo -u postgres psql db_flaskvuepf -c "GRANT ALL ON ALL SEQUENCES IN SCHEMA public to uflaskvuepf;"
sudo -u postgres psql db_flaskvuepf -c "GRANT ALL ON ALL FUNCTIONS IN SCHEMA public to uflaskvuepf;"

sudo -u postgres psql -c "CREATE USER uflaskvuepftest WITH ENCRYPTED PASSWORD 'PwDflaskvuepftestSatu1Dua3';"
sudo -u postgres psql -c "CREATE DATABASE db_flaskvuepftest;"


sudo -u postgres psql db_flaskvuepftest -c "GRANT ALL PRIVILEGES ON DATABASE db_flaskvuepftest TO uflaskvuepftest;"
sudo -u postgres psql db_flaskvuepftest -c "GRANT ALL ON SCHEMA public TO uflaskvuepftest;"
sudo -u postgres psql db_flaskvuepftest -c "GRANT ALL ON ALL TABLES IN SCHEMA public to uflaskvuepftest;"
sudo -u postgres psql db_flaskvuepftest -c "GRANT ALL ON ALL SEQUENCES IN SCHEMA public to uflaskvuepftest;"
sudo -u postgres psql db_flaskvuepftest -c "GRANT ALL ON ALL FUNCTIONS IN SCHEMA public to uflaskvuepftest;"

IF need drop db
sudo -u postgres psql -c "DROP DATABASE db_flaskvuepf;"
sudo -u postgres psql -c "DROP USER IF EXISTS uflaskvuepf;"

2.1. SYSTEM FLASK ENVIRONMENT
-------------------------------------------------------------------------------

sudo apt install language-pack-id
sudo dpkg-reconfigure locales

sudo apt install -y python3-venv 
sudo apt install pip

python3 -m pip install --user pipenv

git clone https://github.com/herbew/flaskvuepf.git


IF PRODUCTION
--
	ln -s /root/flaskvuepf/backend /opt/flaskvuepf/backend 
	cd /opt/flaskvuepf/

ELSE
--
	cd /home/<username>/flaskvuepf/

python3 -m venv venvbackend
source venvbackend/bin/activate

sudo apt install dos2unix -y 
cd flaskvuepf/backend

dos2unix backend/utilities/install_os_dependencies.sh
dos2unix backend/utilities/install_python_dependencies.sh
sudo ./backend/utilities/install_os_dependencies.sh install

IF PRODUCTION
--
	source /opt/flaskvuepf/venvbackend/bin/activate
	cd /opt/flaskvuepf/backend 
ELSE
--
	source /home/<username>/flaskvuepf/venvbackend/bin/activate
	cd /home/<username>/flaskvuepf/backend 

sudo -H pip3 install virtualenv
./backend/utilities/install_python_dependencies.sh install


IF PRODUCTION TEST
--
	directory /opt/
ELSE TEST
--
	directory /home/<username>/

source venvbackend/bin/activate
cd backend/tests/
pytest -s

OR

cd backend/tests/
/home/<username>/venvbackend/bin/pytest -s

IF PRODUCTION SHELL
--
	directory /opt/
	/opt/venvbackend/bin/python3 backend/manage.py shell
	
ELSE SHELL
--
	directory /home/<username>/
	/home/<username>/venvbackend/bin/python3 backend/manage.py shell



IF PRODUCTION RUN
--
	directory /opt/
	/opt/venvbackend/bin/python3 backend/run.py
	
ELSE RUN
--
	directory /home/<username>/
	/home/<username>/venvbackend/bin/python3 backend/run.py
	

 * Serving Flask app 'run'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8080
 * Running on http://192.168.0.155:8080
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 105-089-458


3. SETUP GUNICORN
--------------------------------------------------------------------------------
pip install -r requirements/production.txt

gunicorn --bind 0.0.0.0:8080 wsgi:app

[2023-06-26 03:28:13 +0000] [1595] [INFO] Starting gunicorn 20.1.0
[2023-06-26 03:28:13 +0000] [1595] [INFO] Listening at: http://127.0.0.1:8000 (1595)
[2023-06-26 03:28:13 +0000] [1595] [INFO] Using worker: sync
[2023-06-26 03:28:13 +0000] [1596] [INFO] Booting worker with pid: 1596


sudo vi /etc/systemd/system/gunicorn.service

# Assume the user 'herbew'
# Assume the project directory '/home/herbew/flaskvuepf/backend'
# Assume the environment project directory '/home/herbew/flaskvuepf/venvbackend/bin'

-------------------------------------------------------------------------------
[Unit]
Description=Gunicorn instance to serve messaging
After=network.target

[Service]
User=herbew
Group=www-data
WorkingDirectory=/home/herbew/flaskvuepf/backend
Environment="PATH=/home/herbew/flaskvuepf/venvbackend/bin"
ExecStart=/home/herbew/flaskvuepf/venvbackend/bin/gunicorn --access-logfile - --workers 3 --bind unix:flask.sock -m 007 wsgi:app

[Install]
WantedBy=multi-user.target
-------------------------------------------------------------------------------

sudo systemctl start gunicorn

# Generate sock 'unix:flask.sock' or beed changed and activated the workers
sudo systemctl enable gunicorn	

Created symlink /etc/systemd/system/multi-user.target.wants/gunicorn.service → /etc/systemd/system/gunicorn.service.

sudo systemctl status gunicorn

--
● gunicorn.service - Gunicorn instance to serve messaging
     Loaded: loaded (/etc/systemd/system/gunicorn.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2023-06-26 03:55:07 UTC; 45s ago
   Main PID: 1776 (gunicorn)
      Tasks: 4 (limit: 1012)
     Memory: 60.0M
        CPU: 273ms
     CGroup: /system.slice/gunicorn.service
             ├─1776 /home/herbew/flaskvuepf/venvbackend/bin/python3 /home/herbew/flaskvuepf/venvbackend/bin/gunicorn --access-logfile - --workers 3 --bind unix:flask.sock -m>
             ├─1777 /home/herbew/flaskvuepf/venvbackend/bin/python3 /home/herbew/flaskvuepf/venvbackend/bin/gunicorn --access-logfile - --workers 3 --bind unix:flask.sock -m>
             ├─1778 /home/herbew/flaskvuepf/venvbackend/bin/python3 /home/herbew/flaskvuepf/venvbackend/bin/gunicorn --access-logfile - --workers 3 --bind unix:flask.sock -m>
             └─1779 /home/herbew/flaskvuepf/venvbackend/bin/python3 /home/herbew/flaskvuepf/venvbackend/bin/gunicorn --access-logfile - --workers 3 --bind unix:flask.sock -m>

Jun 26 03:55:07 fub2204 systemd[1]: Started Gunicorn instance to serve messaging.
Jun 26 03:55:07 fub2204 gunicorn[1776]: [2023-06-26 03:55:07 +0000] [1776] [INFO] Starting gunicorn 20.1.0
Jun 26 03:55:07 fub2204 gunicorn[1776]: [2023-06-26 03:55:07 +0000] [1776] [INFO] Listening at: unix:flask.sock (1776)
Jun 26 03:55:07 fub2204 gunicorn[1776]: [2023-06-26 03:55:07 +0000] [1776] [INFO] Using worker: sync
Jun 26 03:55:07 fub2204 gunicorn[1777]: [2023-06-26 03:55:07 +0000] [1777] [INFO] Booting worker with pid: 1777
Jun 26 03:55:07 fub2204 gunicorn[1778]: [2023-06-26 03:55:07 +0000] [1778] [INFO] Booting worker with pid: 1778
Jun 26 03:55:07 fub2204 gunicorn[1779]: [2023-06-26 03:55:07 +0000] [1779] [INFO] Booting worker with pid: 1779
--

ps ax |grep py

--
648 ?        Ss     0:00 /usr/bin/python3 /usr/bin/networkd-dispatcher --run-startup-triggers
708 ?        Ssl    0:00 /usr/bin/python3 /usr/share/unattended-upgrades/unattended-upgrade-shutdown --wait-for-signal
1776 ?        Ss     0:00 /home/herbew/flaskvuepf/venvbackend/bin/python3 /home/herbew/flaskvuepf/venvbackend/bin/gunicorn --access-logfile - --workers 3 --bind unix:flask.sock -m 007 wsgi:app
1777 ?        S      0:00 /home/herbew/flaskvuepf/venvbackend/bin/python3 /home/herbew/flaskvuepf/venvbackend/bin/gunicorn --access-logfile - --workers 3 --bind unix:flask.sock -m 007 wsgi:app
1778 ?        S      0:00 /home/herbew/flaskvuepf/venvbackend/bin/python3 /home/herbew/flaskvuepf/venvbackend/bin/gunicorn --access-logfile - --workers 3 --bind unix:flask.sock -m 007 wsgi:app
1779 ?        S      0:00 /home/herbew/flaskvuepf/venvbackend/bin/python3 /home/herbew/flaskvuepf/venvbackend/bin/gunicorn --access-logfile - --workers 3 --bind unix:flask.sock -m 007 wsgi:app
1859 pts/0    S+     0:00 grep --color=auto py
--
	
	
4. SETUP NGINX
--

sudo apt install nginx

sudo cp -f /home/herbew/flaskvuepf/backend/configs/nginx/local-nginx.conf /etc/nginx/sites-available/flaskvuepf/backend
sudo ln -s /etc/nginx/sites-available/flaskvuepf/backend /etc/nginx/sites-enabled

sudo nginx -t

--
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
--

sudo service nginx configtest

sudo systemctl enable nginx
sudo systemctl start nginx
sudo systemctl restart nginx
sudo systemctl daemon-reload
sudo systemctl status nginx


sudo systemctl restart gunicorn
sudo systemctl restart nginx

IF ANY error
--
2023/06/26 04:47:43 [notice] 2779#2779: using inherited sockets from "6;7;"
2023/06/26 04:55:20 [crit] 3205#3205: *2 connect() to unix:/home/herbew/messaging/flask.sock failed (13: Permission denied) while connecting to upstream, client: 192.168.0.186, server: localhost, request: "GET / HTTP/1.1", upstream: "http://unix:/home/herbew/messaging/flask.sock:/", host: "192.168.0.155:8080"

with sock files:
--
srwxrwx---  1 herbew www-data    0 Jun 26 05:02 flask.sock


assume account is 'herbew'

sudo vi /etc/nginx/nginx.conf
--
#user www-data;
user herbew;
worker_processes auto;
pid /run/nginx.pid;
include /etc/nginx/modules-enabled/*.conf;
...

5. FLASK CONFIGURATION
--
# Assume the project directory '/home/herbew/flaskvuepf/backend'
cp -f /home/herbew/flaskvuepf/backend/default.env /home/herbew/flaskvuepf/backend/.env












