from django.shortcuts import render
import requests
from .services import csv_a_diccionario, ticket_valido, get_coordenadas, get_nombres, validar_ciudad
from django.conf import settings
from django.core.cache import cache


def get_coordenadas_gc(city, appid):
    """
    Obtiene las coordenadas geográficas de una ciudad utilizando la API de OpenWeatherMap.

    Args:
        city (str): Nombre de la ciudad.
        appid (str): Clave de la API de OpenWeatherMap.

    Returns:
        tuple: Latitud y longitud de la ciudad o un mensaje de error si no se puede localizar.
    """
    try:
        geoUrl = "http://api.openweathermap.org/geo/1.0/direct"
        geoParams = {'q': city, 'appid': appid}
        geoResp = requests.get(url=geoUrl, params=geoParams)
        geoResp.raise_for_status()
        djsonGC = geoResp.json()
        if geoResp.status_code == 401:
            return city, "API key no válida o expirada."
        if djsonGC and isinstance(djsonGC, list) and 'lat' in djsonGC[0] and 'lon' in djsonGC[0]:
            lat = djsonGC[0]['lat']
            lon = djsonGC[0]['lon']
            return lat, lon
        else:
            return city, "No se pudo localizar."
    except requests.exceptions.RequestException:
        return city, "Error al conectarse a la API."


def obtener_clima(lat, lon, appid, idioma='es'):
    """
    Obtiene la información climática de una ubicación geográfica usando la API de OpenWeatherMap.

    Args:
        lat (float): Latitud de la ubicación.
        lon (float): Longitud de la ubicación.
        appid (str): Clave de la API de OpenWeatherMap.
        idioma (str): Idioma de la respuesta (por defecto 'es').

    Returns:
        tuple: Temperatura, humedad, presión, velocidad del viento, descripción del clima, icono del clima.
    """
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        'lat': lat,
        'lon': lon,
        'appid': appid,
        'lang': idioma
    }

    try:
        response = requests.get(url, params=params, timeout=20)
        response.raise_for_status()
        data = response.json()
        clima = data['weather'][0]
        return (
            data['main']['temp'],
            data['main']['humidity'],
            data['main']['pressure'],
            data['wind']['speed'],
            clima['description'],
            clima['icon']
        )
    except requests.RequestException as e:
        return str(e), None, None, None, None, None


def obtener_datos_ciudad(lat, lon, appid, cache_key):
    """
    Obtiene y almacena en caché la información climática de una ciudad utilizando las coordenadas geográficas.

    Args:
        lat (float): Latitud de la ciudad.
        lon (float): Longitud de la ciudad.
        appid (str): Clave de la API de OpenWeatherMap.
        cache_key (str): Clave para almacenar los datos en caché.

    Returns:
        dict: Información climática de la ciudad.
    """
    datos = cache.get(cache_key)
    if datos is not None:
        return datos
    
    tempK, humidity, pressure, wind_speed, description, icon = obtener_clima(lat, lon, appid)
    
    if isinstance(tempK, str) and 'Error' in tempK:
        return {'error_message': tempK}
    
    tempC = round(tempK - 273.15, 2)
    datos_nuevos = {
        'tempC': tempC,
        'humidity': humidity,
        'pressure': pressure,
        'wind_speed': wind_speed,
        'description': description,
        'icon': icon
    }
    cache.set(cache_key, datos_nuevos, 60 * 15)
    
    return datos_nuevos


def manejar_ticket(entrada, appid, diccionario, request):
    """
    Procesa un ticket ingresado, obtiene la información climática de las coordenadas y la presenta.

    Args:
        entrada (str): Número de ticket ingresado.
        appid (str): Clave de la API de OpenWeatherMap.
        diccionario (dict): Diccionario con los datos del ticket.
        request (HttpRequest): Solicitud HTTP del cliente.

    Returns:
        HttpResponse: Página renderizada con la información climática del ticket.
    """
    ticket = entrada
    latO, lonO, latD, lonD = get_coordenadas(ticket, diccionario)
    cityO, cityD = get_nombres(ticket, diccionario)
    
    clave1 = str(latO + lonO)
    clave2 = str(latD + lonD)
    datos1 = cache.get(clave1)
    datos2 = cache.get(clave2)
    
    if datos1 is not None and isinstance(datos1, dict) and datos2 is not None and isinstance(datos2, dict):
        datos3 = {**datos1, **datos2}
    else: 
        if datos1 is None:
            tempK, humidity, pressure, wind_speed, description, icon = obtener_clima(latO, lonO, appid)
            tempC = round(tempK - 273.15, 2)
            datos1 = {'cityO': cityO,
                      'tempC': tempC,
                      'humidity': humidity,
                      'pressure': pressure,
                      'wind_speed': wind_speed,
                      'icon': icon,
                      'description': description}
            cache.set(clave1, datos1, 60*15)
                    
        if datos2 is None:    
            tempKD, humidityD, pressureD, wind_speedD, descriptionD, iconD = obtener_clima(latD, lonD, appid)
            tempCD = round(tempKD - 273.15, 2)
            datos2 = {'cityD': cityD,
                      'tempCD': tempCD,
                      'humidityD': humidityD,
                      'pressureD': pressureD,
                      'wind_speedD': wind_speedD,
                      'iconD': iconD,
                      'descriptionD': descriptionD}
            cache.set(clave2, datos2, 60*15)
                        
        datos3 = {**datos1, **datos2}
                
    datos3['ticket_input'] = '¡Buen Viaje!'
    return render(request, 'TreeWeather_app/index.html', datos3)


def manejar_ciudad(entrada, appid):
    """
    Valida una ciudad ingresada y obtiene la información climática correspondiente.

    Args:
        entrada (str): Nombre de la ciudad ingresada.
        appid (str): Clave de la API de OpenWeatherMap.

    Returns:
        dict: Información climática de la ciudad o un mensaje de error si no es válida.
    """
    city = validar_ciudad(entrada)
    if city == 'ciudadInvalida':
        return {'entrada': entrada, 'error_message': 'Ciudad o Ticket no encontrados'}
    
    lat, lon = get_coordenadas_gc(city, appid)
    if isinstance(lon, str) and 'Error' in lon:
        return {'error_message': lon}
    
    clave = f"{lat}{lon}"
    datos = obtener_datos_ciudad(lat, lon, appid, clave)
    if 'error_message' in datos:
        return datos  
    
    datos.update({'city_input': "Se ingresó una ciudad", 'city': city})
    
    return datos




def index(request):
    if request.method != 'POST':
        return render(request, 'TreeWeather_app/index.html', {'entrada': None})

    entrada = request.POST.get('city', '')
    if not entrada:
        return render(request, 'TreeWeather_app/index.html', {
            'entrada': entrada,
            'error_message': 'Inserte el nombre de una ciudad o el número de su ticket.'
        })

    appid = settings.API_KEY
    diccionario = csv_a_diccionario('TreeWeather_app/data/samples.txt')  #aqui se debe cambiar la base de datos
    is_ticket = ticket_valido(diccionario, entrada)

    if is_ticket:
        return manejar_ticket(entrada, appid, diccionario, request)
    else:
        datos = manejar_ciudad(entrada, appid)

    return render(request, 'TreeWeather_app/index.html', datos)
