from django.urls import path
from . import views

urlpatterns = [
    path('', views.load_page),
    path('save_settings/', views.save_settings, name='save_settings'),
]
