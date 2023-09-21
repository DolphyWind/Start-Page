from django.urls import path
from . import views

urlpatterns = [
    path('', views.load_page, name="main"),
    path('save_settings/', views.save_settings, name='save_settings'),
    path('settings/', views.settings, name="settings")
]
