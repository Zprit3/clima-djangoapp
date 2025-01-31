import requests, os
from django.shortcuts import render
from .models import Ciudad
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')

def index(request):
    clima_data = []
    error_message = None

    if request.method == 'POST':
        ciudad_nombre = request.POST.get('ciudad')
        if ciudad_nombre:
            try:
                ciudad = Ciudad.objects.get(nombre__iexact=ciudad_nombre)
            except Ciudad.DoesNotExist:
                try:
                    url = f'http://api.openweathermap.org/data/2.5/weather?q={ciudad_nombre}&appid={API_KEY}'
                    response = requests.get(url)
                    data = response.json()
                    if data['cod'] == 200:
                        ciudad = Ciudad.objects.create(nombre=ciudad_nombre)
                    else:
                        raise Ciudad.DoesNotExist
                except Ciudad.DoesNotExist:
                    error_message = f"No se encontró la ciudad '{ciudad_nombre}'. Intenta con otro nombre."
            if not error_message:
                url = f'http://api.openweathermap.org/data/2.5/weather?q={ciudad.nombre}&appid={API_KEY}&units=metric&lang=es'
                response = requests.get(url)
                data = response.json()

                if data['cod'] == 200:
                    clima = {
                        'ciudad': ciudad.nombre,
                        'temperatura': data['main']['temp'],
                        'descripcion': data['weather'][0]['description'],
                        'icono': data['weather'][0]['icon'],
                    }
                    clima_data.append(clima)
                else:
                    error_message = f"Error al obtener datos para {ciudad.nombre}: {data['message']}"
        else:
            error_message = "Por favor, ingresa el nombre de una ciudad."

    contexto = {
        'clima_data': clima_data,
        'error_message': error_message,
        'API_KEY': API_KEY
    }
    return render(request, 'weather/index.html', contexto)