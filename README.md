Test CHR - Febrero 2023

Requerimientos

Tarea 1

Dada la siguiente API pública http://api.citybik.es/v2/networks/bikesantiago (Bike Santiago)
desarrolle los siguiente requerimientos:

1- Crear una función que obtenga la información presentada en la API pública (librerías a utilizar: requests, urllib3 o aiohttp).

Para cumplir con este requerimiento se creo un projecto en Django versión 4.1.7, llamado "bikesantiago".

Se creo la app "bikes_info" a fin de administrar la información requerida a través del proyecto. Escogimos utilizar la librería requests.

Luego de revisar la información de la API en internet, creamos un archivo utils.py dentro de la app bikes_info, a fin de realizar algunas tareas. Por ejemplo, imprimir de forma amigable la información y así poder definir que elementos de la API debíamos recolectar. Para ello utilizamos la función utils.printdata. Esta función escribe el objecto JSON en un formato amigable en el archivo bikes_data.txt ubicado en la carpeta raíz del proyecto.

2 - Crear un modelo para la información obtenida.

Luego de analizar la información, creamos el modelo en el archivo bikes_info/models.py. Tomamos prácticamente todos los datos relacionados con las estaciones de bicicletas.

Luego de analizar la estructura del objeto JSON de la API, creamos el modelo teniendo en cuenta el tipo de datos correspondiente a cada campo.

En el caso del campo "payment", dado que el mismo contiene una lista con elementos acotados, decidimos utilizar un campo ArrayField para incluir la lista de elementos disponibles en ese campo. 

Para analizar la información contenida en la lista "payment" creamos otra función incluida en utils.py. La función utils.get_payment_choices. Esta función obtiene la información proveniente del objeto JSON de la API, iterando sobre cada registro y extrayendo la lista de elementos en cada campo "payment". Estos resultados se añaden a un set a fin de obtener una lista sin elementos repetidos. El resultado fue que este elemento únicamente contiene las siguientes cadenas de texto: "key", "transitcard", "creditcard", y "phone". Por lo tanto se incluyeron únicamente estas opciones en la variable PAYMENT_CHOICES del modelo, que es la que contiene las opciones disponibles en el campo.


3 - Guardar en el modelo la información obtenida desde el API.

Dado que los requerimientos indican que hay que usar una base de datos PostgreSQL, se instaló el paquete psycopg2-binary==2.9.3. Luego creamos una base de datos en psql llamada bikedb, e incluimos la configuración correspondiente en el archivo settings.py. Se realizaron las migraciones del modelo y se ejecutó el comando migrate, para generar las tablas en la base de datos.

Se creó una nueva función en el archivo utils.py. La función populate_stations. Esta función realiza un GET request a la API y obtiene la información del objeto JSON. Luego de convertirla a un diccionario de Python a través del método .json() proveniente de la librería requests, la información es asignada a la variable json_data.

Luego iteramos sobre cada uno de los registros del diccionario. La función en cada iteración crea una instancia del modelo Station y asigna la información proveniente del diccionario a cada campo del modelo.

En el caso del campo post_code, se utilizó el método get, a fin de ofrecer un valor por defecto, ya que se detectó que no todos los registos incluyen un valor para dicho campo.

En el caso del campo last_updated, el valor provisto por la API es un valor de tipo tiempo Unix, es decir, representa la cantidad de segundos transcurridos desde el 1/1/1970. Para convertirlo a formato datetime se utilizó el método fromtimestamp proveniente del módulo datetime.

4 - Generar vista en el administrador

Para ello se incluyó en el archivo bikes_info/admin.py la clase StationAdmin, que a su vez hereda las características de la clase admin.ModelAdmin de Django. La clase incluye antes de su encabezado el decorador @admin.register para que Django incluya la información del modelo Station en el administrador de Django.

En esta clase incluimos las siguientes variables: list_display, que incluye los campos visibles al abrir la vista de Stations en el administrador; list_filter, que incluye los campos que permiten filtrar la información; y search_fields, que incluye los campos con los cuales podemos buscar información en la base de datos.

5 - Generar una vista con la información usando Bootstrap 5.

Para esta vista, incluimos una función en el archivo bikes_info/views.py. La función index hace una consulta para obtener todos los objetos de la base de datos, y los transmite a una plantilla (template) de Django. Para dar una apariencia agradable a nuestra plantilla, utilizamos la biblioteca bootstrap. Para ello creamos la carpeta static en la cual se encuentran todos los archivos estáticos de bootstrap, css y js.

Instrucciones de ejecución

Para ejecutar el proyecto es necesario contar con el administrador de base de datos PostgreSQL.

Pasos a seguir:

- Crear una carpeta para guardar los archivos del proyecto
- Crear un virtual environment
- Activar el virtual environment
- Clonar el repositorio
- Instalar los paquetes (pip install -r requirements.txt)
- Realizar y ejecutar las migraciones (python manage.py makemigraitons, python manage.py migrate)
- Abrir el shell (python manage.py shell)
- Ejecutar las siguientes líneas de código en el shell

>>> from bikes_info.utils import populate_stations
>>> populate_stations()

- Salir del shell

Para acceder a la información desde el navegador

- Ejecutar el servidor (python manage.py runserver)
- Abrir la dirección http://127.0.0.1:8000/bikes/

Tarea 2

Dada la siguiente url https://seia.sea.gob.cl/busqueda/buscarProyectoAction.php (Servicio
de Evaluación Ambiental) desarrolle los siguiente requerimientos:

- Crear un script para obtener la información presentada en la tabla de la url proporcionada (librerías a utilizar: BeautifulSoup o Selenium).

Para esta tarea creamos una nueva aplicación llamada seia. Creamos un archivo utils.py para implementar las funciones necesarias. Instalamos los paquetes BeautifulSoup y Selenium. 

- El script deberá recorrer todas las páginas y obtener la información de las tablas.

Luego de analizar la página web, identificamos que había que extraer la información de las tablas utilizando la librería Selenium en conjunto con chromedriver, a fin de acceder a la información de cada página. Al abrir cada página web obtenemos entonces la información de las tablas con la librería BeautifulSoup.

Se crearon tres funciones:

scrape_pages se encarga de la lógica general del programa. Inicialmente genera un web driver disponible en la librería Selenium que se encarga de abrir el navegador de Google Chrome e ir a la página solicitada. La función recibe como argumentos el número de página inicial y final, de manera de tener la opción de extraer datos de un rango de páginas.

La función itera sobre el rango de páginas llamando en cada iteración a la función open_page, pasando los argumentos del driver y de la página de la cuál extraeremos información.

open_page genera un objecto Select disponible en la librería Selenium que nos sirve para manipular el menú desplegable para seleccionar la página. Damos un tiempo de espera para garantizar que la página haya abierto completamente con el método implicitly_wait del driver. Luego se llama a la funcion get_table_data para obtener la información.

get_table_data utiliza la librería BeautifulSoup para obtener datos de la página. Para ello identifica en el código html de la página los elementos que forman parte de la tabla de la cuál vamos a extraer información.

Creamos una lista proyectos para ir guardando la información de cada proyecto que aparece en la tabla. Luego iteramos a través de cada fila de la tabla y obtenemos la información de cada celda. En algunos casos pueden aparecer filas que no contienen información, y las saltamos para que la información cuadre con los encabezados.

Creamos un diccionario proyecto y guardamos los datos según su clave. Finalmente añadimos el diccionario a la lista proyectos.

- El script deberá crear un archivo .json con la información obtenida.

Luego de cada iteración anexamos los elementos a un archivo json. Dado que cada iteración genera una lista, fue necesario generar una lógica para que el resultado final fuera un objeto json válido, por ello, la primera vez que se agrega información al archivo debemos escribir un corchete de apertura. Dado que al final de cada iteración se genera un corchete, al añadir nueva información hay que borrar ese corchete, añadir una coma, y borrar el primer corchete de la nueva información. De esta forma obtenemos un objeto json válido.


- Generar modelo para guardar la información obtenida.

Luego de identificar los datos creamos el modelo en el archivo seia/models.py, de acuerdo a los tipos de datos adecuados. Realizamos las migraciones.

Se creó también la función populate_db_from_json para trasladar los datos del objeto json a la base de datos.

- Opcional. Generar vista en el administrador para visualizar la información obtenida.

Se configuró el archivo seia/admin.py para mostrar la información del modelo en el administrador de Django.


- Opcional. Generar una vista con la información en Bootstrap 5 u otro similar.

Se creo una función en el archivo seia/views.py para mostrar la información en el navegador. Igualmente se generaron las urls correspondientes, tanto en el archivo seia/urls.py como en el archivo del proyecto bikesantiago/urls.py. También se incluyó la plantilla (template) para mostrar la información, la cual fue decorada con la bilioteca bootstrap.

Instrucciones de ejecución

Para ejecutar el proyecto es necesario contar con el administrador de base de datos PostgreSQL.

Pasos a seguir:

- Crear una carpeta para guardar los archivos del proyecto
- Crear un virtual environment
- Activar el virtual environment
- Clonar el repositorio
- Instalar los paquetes (pip install -r requirements.txt)
- Realizar y ejecutar las migraciones (python manage.py makemigraitons, python manage.py migrate)
- Abrir el shell (python manage.py shell)
- Ejecutar las siguientes líneas de código en el shell

>>> from seia.utils import *

Para extraer la información de la página https://seia.sea.gob.cl/busqueda/buscarProyectoAction.php.

- Es necesario contar con el archivo seiadata.json en el directorio raíz. El archivo puede estar vacío. Si se descargan las páginas por rangos, la información se anexa al final del archivo.

>>> scrape_pages(1, 2846)  # usar el rango que se desee extraer


Para trasladar los datos del archivo json a la base de datos

>>> from seia.utils import *
>>> populate_db_from_json('seiadata.json')

Para acceder a la información desde el navegador

- Ejecutar el servidor (python manage.py runserver)
- Abrir la dirección http://127.0.0.1:8000/seia/