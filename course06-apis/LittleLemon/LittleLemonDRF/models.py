from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        indexes = [
            models.Index(fields=['price']),
        ]



from django.urls import path
from . import views

urlpatterns = [
    path('books',views.books),
    # path('books/<int:pk>',views.book),
]

# Solution code for urls.py (app-level):
