from django.urls import path
from . import views
from .views import ProjectDetailView

urlpatterns = [
    path('', views.home, name='feria_ing-home'),
    path('search/', views.search_bar, name="feria_ing-search"),
    path('project/<int:pk>/', ProjectDetailView.as_view(), name="project-detail")
]