from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
import getpass
import geocoder
import requests
import datetime

# Create your views here.
def get_weather_stats():
    g = geocoder.ip('me')
    lat, lon = g.latlng
    
    # Get sunset and sunrise times
    url_sunset_sunrise = f'https://api.sunrise-sunset.org/json?lat={lat}&lng={lon}&formatted=0'
    try:
        req = requests.get(url_sunset_sunrise)
    except:
        pass
    
    isday = True
    if req.status_code == 200:
        data = req.json()
        if data['status'] == 'OK':
            data = data['results']
            
            sunrise = data['sunrise'].rsplit('+', 1)[0]
            sunset = data['sunset'].rsplit('+', 1)[0]
            
            sunrise = datetime.datetime.strptime(sunrise, '%Y-%m-%dT%H:%M:%S')
            sunset = datetime.datetime.strptime(sunset, '%Y-%m-%dT%H:%M:%S')
            
            utc_now = datetime.datetime.utcnow()
            if utc_now >= sunrise and utc_now <= sunset:
                isday = True
            else:
                isday = False
    
    dn_class = 'wu-day' if isday else 'wu-night'
    
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    try:
        req = requests.get(url)
    except:
        pass
    if req.status_code == 200:
        data = req.json()
        temperature = data['current_weather']['temperature']
        weather_code = data['current_weather']['weathercode']
        weather_class = 'wu-unknown'
        
        if weather_code in (0, 1):
            weather_class = 'wu-clear'
        elif weather_code == 2:
            weather_class = 'wu-partlycloudy'
        elif weather_code == 3:
            weather_class = 'wu-cloudy'
        elif weather_code in (45, 48):
            weather_class = 'wu-fog'
        elif weather_code in (51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82):
            weather_class = 'wu-rain'
        elif weather_code in (71, 73, 75, 77, 85, 86):
            weather_class = 'wu-snow'
        elif weather_code in (95, 96, 99):
            weather_class = 'wu-tstorms'
        
        return dn_class, temperature, weather_class
    else:
        return None

def get_dt():
    dt = datetime.datetime.now()
    hour = dt.hour
    part_of_day = None
    dt_str = dt.strftime('%d/%m/%Y')

    if hour >= 5 and hour < 12:
        part_of_day = 'Morning'
    elif hour >= 12 and hour < 17:
        part_of_day = 'Afternoon'
    elif hour >= 17 and hour < 21:
        part_of_day = 'Evening'
    else:
        part_of_day = 'Night'
    
    return dt_str, part_of_day

def load_page(request):
    context_data = dict()
    context_data['name'] = getpass.getuser()
    
    dn_class, temperature, weather_class = get_weather_stats()
    context_data['dn_class'] = dn_class
    context_data['temperature'] = temperature
    context_data['weather_class'] = weather_class
    
    dt_str, part_of_day = get_dt()
    context_data['dt_str'] = dt_str
    context_data['part_of_day'] = part_of_day
    
    return render(request, 'mainpage.html', context_data)