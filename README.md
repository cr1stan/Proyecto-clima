# Proyecto-clima
![alt text](image.png)

## Integrantes:
- Urzua Contreras Cristian Josue - Lider
- Rosas Marín Jesús Martín - BackEnd
- Reyes Arteaga Angel David - FrontEnd

### Pasos para correr el programa

1. **Clona el repositorio**:
   ```
   git clone https://github.com/cr1stan/Proyecto-clima.git
   ```
   
2. **Abre el directorio desde la terminal**:
   ```
   cd Proyecto-clima\TreeWeather
   ```
3. **Instala `pip`:**

   Para poder instalar paquetes de python necesarios para el funcionamiento correcto de la app de clima.

     - En Windows:

       Descarga el archivo `get-pip.py` desde el sitio oficial de Python. Puedes hacerlo desde el navegador o desde la linea de comandos con:

        ```
        curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
        ```

       Asegurate de estar en el directorio donde descargaste `get-pip.py`, para ejecutar el archivo :

       ```
       python get-pip.py
       ```

       Sigue las instrucciones en pantalla para completar la instalación.
       
      - En MacOS:

        Ejecuta el siguiente comando en la terinal para descargar el script de instalación de `pip`:

        ```
        curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
        ```

         Ahora ejecuta la el script de instalción con python:

        ```
         python get-pip.py
        ```
        Sigue las instrucciones en pantalla para completar la instalación.
      - Linux:

        En la mayoria de las distribuciones ya vienen con  `pip` preinstalado. Sin embargo, si no lo tienes instalado o deseas     actualizarlo, puedes usar el administrador de paquetes de tu distribución para instalarlo.
  

5. **Configura el entorno virtual**:

   a. Instala `virtualenv` si aún no lo tienes:
      ```
      pip install virtualenv
      ```

   b. Crea un entorno virtual:
      ```
      virtualenv nombre_del_entorno
      ```

   c. Activa el entorno virtual:
      - En Windows:
        ```
        .\nombre_del_entorno\Scripts\activate
        ```
      - En MacOS/Linux:
        ```
        source nombre_del_entorno/bin/activate
        ```

6. **Instala los requisitos del proyecto**:

   En la ruta  ```Proyecto-clima\TreeWeather ``` y con el entorno virtual activado.

   ```
   pip install -r requirements.txt
   ```
7. **Configura la API Key de OpenWeathermap:**

   > <b>Este paso es importante para el funcionamiento correcto de la app.</b>

   a. En la ruta  ```Proyecto-clima\TreeWeather\TreeWeather/settings.py ```.
   
   b. Dentro del archivo ```settings.py ```, en la ultima linea agrega tu key en donde dice ```API_KEY=''```.
   
   c. Dentro de las comillas simples que están en la linea debajo de la etiqueta, agrega tu API Key.

   > Para obtener tu API Key, da click en <b>[API Key](https://openweathermap.org/price)</b>  y haz scroll hasta  la sección de <b>Current weather and forecasts collection</b> y luego en <b>Get API Key</b>.


8. **Corre el servidor de desarrollo de Django**:
   ```
   python manage.py runserver
   ```

   Esto iniciará el servidor, y deberas poder acceder a la aplicación en `http://127.0.0.1:8000/` en tu navegador.

### Para desactivar el entorno virtual

Ya que has terminado de interactuar con nuestra App  desactiva el entorno virtual, para ello corre lo siguiente en tu terminal:

 ```
   deactivate
 ```

Y asi el entorno virtual acaba de desactivarse.
