from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from .Globals import globals
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def save_settings(request):
    if request.method == "GET":
        globals.settings_manager.save_settings()
        return HttpResponse(200, "Save Successfull!")
    elif request.method == "POST":
        for key, value in json.loads(request.body.decode()).items():
            globals.settings_manager[key] = value

        globals.settings_manager.save_settings()
        return HttpResponse(200, "Save Successfull!")

@csrf_exempt
def reset_settings(request):
    print("reset")
    globals.settings_manager.reset_settings()
    globals.settings_manager.save_settings()
    return HttpResponse(200)

def load_page(request):
    globals.fetch()
    return render(request, 'mainpage.html', globals.get_context_data())

def settings(request):
    globals.fetch()
    return render(request, "settings.html", globals.get_context_data())