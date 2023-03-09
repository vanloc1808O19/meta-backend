from django.urls import path, re_path
from . import views 

urlpatterns = [ 
    path("home/", views.home),
    path("dishes/<str:dish>", views.dishes), # dish = pasta
    re_path(r"^menu_item/([0-9]{2})/$", views.display_menu_item), # menu_item/01
] 