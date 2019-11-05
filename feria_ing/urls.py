from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='feria_ing-home'),
    path('login/', views.login, name='feria_ing-login')
]