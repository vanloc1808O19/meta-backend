# sudo apt-get update
# python3 -m venv ./env
# source env/bin/activate
# pip install django
# source env/bin/activate
# django-admin startproject little_lemon 
cd little_lemon  
# python3 manage.py startapp restaurant
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver