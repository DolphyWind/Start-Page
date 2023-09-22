from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from .Globals import globals

# Called automatically when user leaves the website
def save_settings(request):
    globals.settings_manager.save_settings()
    return HttpResponse(200, "Save Successfull!")

def load_page(request):
    globals.fetch()
    return render(request, 'mainpage.html', globals.get_context_data())

def settings(request):
    globals.fetch()
    return render(request, "settings.html", globals.get_context_data())