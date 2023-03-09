from django.contrib import admin
from .models import *
# Import the models from models.py

# Register your models here.
admin.site.register(DrinksCategory)
admin.site.register(Drinks)