# sudo apt-get update
# python3 -m venv ./env
# source env/bin/activate
# pip install django
cd demoproject 
source env/bin/activate
# django-admin startproject demoproject 
# cd demoproject 
# python manage.py startapp demoapp
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver