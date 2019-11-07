from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='feria_ing-home'),
    path('search/', views.search_bar, name="feria_ing-search")
]