from django.urls import path
from . import views
from .views import (ProjectDetailView ,ProjectCreateView)

urlpatterns = [
    path('', views.home, name='feria_ing-home'),
    path('unirse/', views.unirse_proyecto, name='unirse_proyecto'),
    path('salir/', views.salir_projecto, name='salir-proyecto'),
    path('search/', views.search_bar, name="feria_ing-search"),
    path('evaluar/', views.evauluar, name ='evaluar'),
    path('leaderboard/', views.leaderboard, name ='leaderboard'),
    path('project/new/', ProjectCreateView.as_view(), name="project-create"),
    path('project/<int:pk>/', ProjectDetailView.as_view(), name="project-detail"),
    path('categoria/<str:categoria>/', views.cat_projs, name="categoria"),
]
