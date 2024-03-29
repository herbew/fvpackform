## Flask Vue PackForm 
#### For Ubuntu 22.04
Clone this repository with <b>*git clone https://github.com/herbew/fvpackform.git*</b>.</br>
We have 2 modules, on directory <b>*fvpackform*</b>
### 1. Backend 
##### 1.1. Install Database
```
sudo apt update
sudo apt install postgresql postgresql-contrib
```
Database
```
sudo -u postgres psql -c "CREATE USER ufvpackform WITH ENCRYPTED PASSWORD 'PwDfvpackformSatu1Dua3';"
```
```
sudo -u postgres psql -c "CREATE DATABASE db_fvpackform;"
sudo -u postgres psql db_fvpackform -c "GRANT ALL PRIVILEGES ON DATABASE db_fvpackform TO ufvpackform;"
sudo -u postgres psql db_fvpackform -c "GRANT ALL ON SCHEMA public TO ufvpackform;"
sudo -u postgres psql db_fvpackform -c "GRANT ALL ON ALL TABLES IN SCHEMA public to ufvpackform;"
sudo -u postgres psql db_fvpackform -c "GRANT ALL ON ALL SEQUENCES IN SCHEMA public to ufvpackform;"
sudo -u postgres psql db_fvpackform -c "GRANT ALL ON ALL FUNCTIONS IN SCHEMA public to ufvpackform;"
```
Database Test
```
sudo -u postgres psql -c "CREATE USER ufvpackformtest WITH ENCRYPTED PASSWORD 'PwDfvpackformtestSatu1Dua3';"
```
```
sudo -u postgres psql -c "CREATE DATABASE db_fvpackformtest;"
sudo -u postgres psql db_fvpackformtest -c "GRANT ALL PRIVILEGES ON DATABASE db_fvpackformtest TO ufvpackformtest;"
sudo -u postgres psql db_fvpackformtest -c "GRANT ALL ON SCHEMA public TO ufvpackformtest;"
sudo -u postgres psql db_fvpackformtest -c "GRANT ALL ON ALL TABLES IN SCHEMA public to ufvpackformtest;"
sudo -u postgres psql db_fvpackformtest -c "GRANT ALL ON ALL SEQUENCES IN SCHEMA public to ufvpackformtest;"
sudo -u postgres psql db_fvpackformtest -c "GRANT ALL ON ALL FUNCTIONS IN SCHEMA public to ufvpackformtest;"
```

##### 1.2. Install Environment
```
sudo apt install language-pack-id
```
```
sudo dpkg-reconfigure locales
```
```
sudo apt install -y python3-venv 
sudo apt install pip
sudo apt install dos2unix -y 
```
```
python3 -m pip install --user pipenv
```
```
git clone https://github.com/herbew/fvpackform.git
```
```
cd fvpackform
python3 -m venv venvbackend
```
```
dos2unix backend/utilities/install_os_dependencies.sh
dos2unix backend/utilities/install_python_dependencies.sh
```
```
sudo ./backend/utilities/install_os_dependencies.sh install
```
##### 1.3. Install Application
```
source venvbackend/bin/activate
```
```
sudo -H pip3 install virtualenv
```
```
./backend/utilities/install_python_dependencies.sh install
```
##### 1.3.1. migrations database
```
cd backend
```
```
cp default.env .env
```
```
python3 manage.py db init
```
```
python3 manage.py db migrate
```
```
python3 manage.py db upgrade
```
##### 1.4. Test
```
python3 test_manage.py db upgrade
```
```
python3 test_manage.py test
```
##### 1.5. Running Service
```
python3 manage.py db_populate
```
```
python3 manage.py runserver
```

### 2. Frontend with Vue 3
#### 2.1. Install Node.js
```
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
source ~/.bashrc
nvm install v20.11.0
```
#### 2.2. Install Vue
```
npm install -g @vue/cli
```
#### 2.3. Run Service
```
cd ../frontend
```
Update the .env variable 
```
vi .env
```
```
VUE_APP_APIURL_SALES_ORDER_ITEM=http://<IP>:<PORT>/admin/api/sales/order/item/list/

```
IP = The IP of backend service run</br>
PORT = The PORT of backend service run

```
npm install
```
```
npm run test:unit
```
```
npm run serve
```














