import unittest
from django.test import TestCase
from services import validar_ciudad, leer_archivo, ticket_valido, csv_a_diccionario, get_coordenadas

class TestValidarCiudad(TestCase):

    def test_ciudad_valida(self):
        self.assertEqual(validar_ciudad("Monterrey"), "Monterrey")

    def test_abreviatura_ciudad(self):
        self.assertEqual(validar_ciudad("MEX"), "Ciudad de Mexico")

    def test_ciudad_parecida(self):
        self.assertEqual(validar_ciudad("Monterei"), "Monterrey")

    def test_ciudad_invalida(self):
        self.assertEqual(validar_ciudad("Atlantis"), "ciudadInvalida")


class TestLeerArchivo(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.mock_data = "data"
        
    def test_archivo_existe(self):
        with unittest.mock.patch('builtins.open', unittest.mock.mock_open(read_data=self.mock_data)):
            resultado = leer_archivo('archivo.txt')
            self.assertEqual(resultado, self.mock_data)

    def test_archivo_no_existe(self):
        with unittest.mock.patch('builtins.open', side_effect=FileNotFoundError):
            resultado = leer_archivo('archivo.txt')
            self.assertEqual(resultado, "")


class TestTicketValido(TestCase):

    def test_ticket_existe(self):
        diccionario = {"123": "Ticket 123"}
        self.assertTrue(ticket_valido(diccionario, "123"))

    def test_ticket_no_existe(self):
        diccionario = {"123": "Ticket 123"}
        self.assertFalse(ticket_valido(diccionario, "456"))


class TestGetCoordenadas(TestCase):

    def test_ticket_valido_con_coordenadas(self):
        diccionario = {
            "123": {
                "origin_latitude": "19.4326", 
                "origin_longitude": "-99.1332", 
                "destination_latitude": "34.0522", 
                "destination_longitude": "-118.2437"
            }
        }
        self.assertEqual(get_coordenadas("123", diccionario), ("19.4326", "-99.1332", "34.0522", "-118.2437"))

    def test_ticket_valido_sin_coordenadas(self):
        diccionario = {
            "123": {
                "origin_latitude": "19.4326"
            }
        }
        self.assertEqual(get_coordenadas("123", diccionario), ("123", "Datos incompletos para el ticket", None, None))

    def test_ticket_invalido(self):
        diccionario = {}
        self.assertIn("No es un ticket válido", get_coordenadas("999", diccionario)[1])


class TestCsvADiccionario(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.mock_csv_data = "clave,valor\n123,algo\n456,otro"
    
    def test_csv_a_diccionario(self):
        with unittest.mock.patch('builtins.open', unittest.mock.mock_open(read_data=self.mock_csv_data)):
            resultado = csv_a_diccionario('archivo.csv')
            self.assertEqual(resultado, {"123": {"valor": "algo"}, "456": {"valor": "otro"}})

    def test_archivo_no_encontrado(self):
        with unittest.mock.patch('builtins.open', side_effect=FileNotFoundError):
            resultado = csv_a_diccionario('archivo.csv')
            self.assertEqual(resultado, {})

