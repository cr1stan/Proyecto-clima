import csv
import json
from difflib import get_close_matches


ciudades_validas = [
    "Mexico", "Monterrey", "Guadalajara", "Tampico", "Ciudad Juarez", "Cancun",
    "Mexicali", "Tijuana", "Hermosillo", "Mazatlan", "Puebla", "Veracruz", "Acapulco",
    "Puerto Vallarta", "Queretaro", "Cozumel", "Zihuatanejo", "Toluca", "Torreon",
    "Puerto Escondido", "Chetumal", "Ciudad del Carmen", "Merida", "Ciudad de Mexico",
    "Jalisco", "Leon", "Tlaxcala", "Cuernavaca", "Juarez", "Aguascalientes", "La Paz", 
    "Colima", "Pachuca", "Tula", "San Luis Potosi", "Nuevo Laredo", "Orizaba", "Xalapa",
    "Tulancingo", "Nuevo Leon", "Guanajuato", "Campeche", "Ensenada", "Tapachula", "Durango",
    "Valle de Mexico", "Celaya", "Oaxaca", "Zacatecas", "San Miguel de Allende", "Los Cabos",
    "Silao", "Morelia", "Tepoztlan", "La Marquesa", 
    "Toronto", "Santiago de Chile", "Madrid", "Ciudad Obregon", "Atlanta", "Amsterdam",
    "Houston", "Vancouver", "Charlotte", "Los Angeles", "Phoenix", "Dallas", "Fort Worth",
    "Philadelphia", "Miami", "Lima", "Bogota", "Havana", "Hong Kong", "Londres", 
    "Hawai", "Dublin", "Chicago", "Kuala Lumpur", "Taipei", "Seul", "Pekin", "Shanghai", 
    "Singapur", "Sidney", "Tokio", "Delhi", "Rio de Janeiro", "Jeju", 
    "Yakarta", "Bangkok", "Paris", "Doha", "Estambul", "Cairo", "Dubai", "Roma", 
    "Barcelona", "Osaka", "Denver", "Florida", "Washington D.C.", 
    "Las Vegas", "Santa Monica", "Venecia", "Munich", "Berlin", "Moscu", "Florencia", 
    "Chennai", "Orlando", "Jaipur", "Riyadh", "Johannesburgo", 
    "Johor Bahru", "Viena", "Denpasar", "Milan", "Agra", "Praga", "Mumbai", "Guangzhou", 
    "Shenzhen", "Macao"
]

abreviaciones_ciudades = {
    "MEX": "Ciudad de Mexico", 
    "MTY": "Monterrey", 
    "GDL": "Guadalajara", 
    "TAM": "Tampico", 
    "CJS": "Ciudad Juarez", 
    "CUN": "Cancun",
    "MXL": "Mexicali", 
    "TIJ": "Tijuana", 
    "HMO": "Hermosillo", 
    "MZT": "Mazatlan", 
    "PUE": "Puebla", 
    "VER": "Veracruz", 
    "ACA": "Acapulco",
    "PVR": "Puerto Vallarta", 
    "QRO": "Queretaro", 
    "CZM": "Cozumel", 
    "ZIH": "Zihuatanejo", 
    "TLC": "Toluca", 
    "TRC": "Torreon",
    "PXM": "Puerto Escondido", 
    "CTM": "Chetumal", 
    "CME": "Ciudad del Carmen", 
    "MID": "Merida", 
    "JAL": "Jalisco", 
    "BJX": "Leon",
    "TXC": "Tlaxcala", 
    "CVJ": "Cuernavaca", 
    "JUA": "Juarez", 
    "AGU": "Aguascalientes", 
    "LAP": "La Paz", 
    "CLQ": "Colima",
    "PCH": "Pachuca", 
    "TUA": "Tula", 
    "SLP": "San Luis Potosi", 
    "NLD": "Nuevo Laredo", 
    "ORIZ": "Orizaba", 
    "JALX": "Xalapa",
    "TUA": "Tulancingo", 
    "NL": "Nuevo Leon", 
    "GTO": "Guanajuato", 
    "CPE": "Campeche", 
    "ENS": "Ensenada", 
    "TAP": "Tapachula", 
    "DGO": "Durango",
    "VAL": "Valle de Mexico", 
    "CYW": "Celaya", 
    "OAX": "Oaxaca", 
    "ZCL": "Zacatecas", 
    "SMA": "San Miguel de Allende", 
    "LCO": "Los Cabos",
    "SIL": "Silao", 
    "MLM": "Morelia", 
    "TEP": "Tepoztlan", 
    "LMQ": "La Marquesa", 
    "YYZ": "Toronto", 
    "SCL": "Santiago de Chile",
    "MAD": "Madrid", 
    "CEN": "Ciudad Obregon", 
    "ATL": "Atlanta", 
    "AMS": "Amsterdam", 
    "IAH": "Houston", 
    "YVR": "Vancouver",
    "CLT": "Charlotte", 
    "LAX": "Los Angeles", 
    "PHX": "Phoenix", 
    "DFW": "Dallas", 
    "FTW": "Fort Worth", 
    "PHL": "Philadelphia",
    "MIA": "Miami", 
    "LIM": "Lima", 
    "BOG": "Bogota", 
    "HAV": "Havana", 
    "HKG": "Hong Kong", 
    "LHR": "Londres", 
    "HNL": "Hawai",
    "DUB": "Dublin", 
    "ORD": "Chicago", 
    "KUL": "Kuala Lumpur", 
    "TPE": "Taipei", 
    "ICN": "Seul", 
    "PEK": "Pekin", 
    "PVG": "Shanghai",
    "SIN": "Singapur", 
    "SYD": "Sidney", 
    "HND": "Tokio", 
    "DEL": "Delhi", 
    "GIG": "Rio de Janeiro", 
    "CJU": "Jeju", 
    "CGK": "Yakarta",
    "BKK": "Bangkok", 
    "CDG": "Paris", 
    "DOH": "Doha", 
    "IST": "Estambul", 
    "CAI": "Cairo", 
    "DXB": "Dubai", 
    "FCO": "Roma",
    "BCN": "Barcelona", 
    "KIX": "Osaka", 
    "DEN": "Denver", 
    "FL": "Florida", 
    "WDC": "Washington D.C.", 
    "LAS": "Las Vegas", 
    "SMO": "Santa Monica", 
    "VCE": "Venecia", 
    "MUC": "Munich", 
    "BER": "Berlin", 
    "SVO": "Moscu", 
    "FLR": "Florencia", 
    "MAA": "Chennai", 
    "MCO": "Orlando", 
    "JAI": "Jaipur",
    "RUH": "Riyadh", 
    "JNB": "Johannesburgo", 
    "JHB": "Johor Bahru", 
    "VIE": "Viena", 
    "DPS": "Denpasar", 
    "MXP": "Milan",
    "AGR": "Agra", 
    "PRG": "Praga", 
    "BOM": "Mumbai", 
    "CAN": "Guangzhou", 
    "SZX": "Shenzhen", 
    "MFM": "Macao"
}

def validar_ciudad(ciudad):
    """Valida la ciudad proporcionada con una lista de ciudades válidas. 
    Si se ingresa una abreviatura, se convertirá en su nombre completo.
    Si la ciudad ingresada se parece a un nombre de ciudades_validas en al menos un 0.6 de similitud, 
    se devolverá el nombre de ciudad válido.
    
    Args:
    - ciudad (str): El nombre de la ciudad ingresado por el usuario.
    
    Returns:
    - str: El nombre válido de la ciudad si se encuentra, 'ciudadInvalida' en caso contrario.
    """
    
    ciudad = abreviaciones_ciudades.get(ciudad.upper(), ciudad)
    
    matches = get_close_matches(ciudad, ciudades_validas, n=1, cutoff=0.6)
    
    if matches:
        return matches[0]
    else:
        return 'ciudadInvalida'

def leer_archivo(ruta):
    """Lee el contenido de un archivo y lo devuelve como un string.
    
    Args:
    - ruta (str): La ruta al archivo que se va a leer.
    
    Returns:
    - str: El contenido del archivo como un string.
    """
    try:
        with open(ruta, 'r') as archivo:
            contenido = archivo.read()
        return contenido
    except FileNotFoundError:
        print(f"El archivo '{ruta}' no se encontró.")
        return ""
    except Exception as e:
        print(f"Ocurrió un error: {str(e)}")
        return ""

def ticket_valido(diccionario, clave):
    """Verifica si una clave existe en el diccionario.
    
    Args:
    - diccionario (dict): El diccionario donde se busca la clave.
    - clave (str): La clave que se va a verificar.
    
    Returns:
    - bool: True si la clave existe en el diccionario, False en caso contrario.
    """
    return clave in diccionario

def csv_a_diccionario(archivo):
    """Convierte el contenido de un archivo CSV en un diccionario.
    
    Args:
    - archivo (str): La ruta al archivo CSV.
    
    Returns:
    - dict: Un diccionario que contiene los datos del archivo CSV.
    """
    diccionario = {}
    try:
        with open(archivo, mode='r', newline='') as archivo_csv:
            lector_csv = csv.DictReader(archivo_csv)
            for fila in lector_csv:
                clave = fila.pop(lector_csv.fieldnames[0])
                diccionario[clave] = fila
    except FileNotFoundError:
        print(f"El archivo '{archivo}' no se encontró.")
    except Exception as e:
        print(f"Ocurrió un error: {str(e)}")
    return diccionario

def obtener_coordenadas(ticket, diccionario): 
    """Recupera las coordenadas de origen y destino de un ticket.
    
    Args:
    - ticket (str): El ticket para el que se van a recuperar las coordenadas.
    - diccionario (dict): El diccionario que contiene los datos.
    
    Returns:
    - tuple: Un tuple que contiene las coordenadas de origen y destino.
    """
    if ticket_valido(diccionario, ticket):
        if ('origin_latitude' in diccionario[ticket] and 'origin_longitude' in diccionario[ticket] and
            'destination_latitude' in diccionario[ticket] and 'destination_longitude' in diccionario[ticket]):
            latO = diccionario[ticket]['origin_latitude']
            lonO = diccionario[ticket]['origin_longitude']
            latD = diccionario[ticket]['destination_latitude']
            lonD = diccionario[ticket]['destination_longitude']
            return latO, lonO, latD, lonD
        else:
            return ticket, "Datos incompletos para el ticket", None, None
    return ticket, f"{ticket} No es un ticket válido en:\n{json.dumps(diccionario)}", None, None

def obtener_nombres(ticket, diccionario):
    """Recupera los nombres de las ciudades de origen y destino de un ticket.
    
    Args:
    - ticket (str): El ticket para el que se recuperan los nombres de las ciudades.
    - diccionario (dict): El diccionario que contiene los datos.
    
    Returns:
    - tuple: Un tuple que contiene los nombres de las ciudades de origen y destino.
    """
    if ticket_valido(diccionario, ticket):
        cityO = diccionario[ticket].get('origin', 'Desconocido')
        cityD = diccionario[ticket].get('destination', 'Desconocido')
        return cityO, cityD
    return "Ticket no válido", "Ticket no válido"
