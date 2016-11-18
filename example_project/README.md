==============================
djangocms-rest-api example app
==============================

Test application for Django Cms Rest Api

Django app
----------

* create virtualenv with: virtualenv venv
* activate env with: source venv/bin/activate
* install requirement with: pip install -r requirements.txt
* call migrations: ./manage.py migrate
* create a superuser ./manage.py createsuperuser
* run dev server: ./manage.py runserver
 
You can access api via http://localhost:8000/en/api/

React app
---------

To start project you need node version 6 or more
* open a new terminal window
* navigate to the react-app
* npm install
* npm start

Please not that Django dev server should be running on 127.0.0.1:8000
If you need another endpoint you can specify it in API_ENDPOINT param
in react-app/src/constants/Constants.js


