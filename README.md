# Indeed Web Scraper
Indeed Web Scrapper es un script que se encarga de recoger los datos de las ofertas de trabajo de _Data scientist_ en Barcelona que se suben a [indeed.com](https://es.indeed.com), y almacenarlos en un CSV. Así evitas tener de recorrer las cientos de ofertas de trabajo que permanecen en la web.

El trabajo forma parte de la Practica 1 de la asignatura _Tipología y ciclo de vida de los datos_, del Máster en Ciencia de Datos de la Universitat Oberta de Catalunya.

## Miembros del equipo

Se ha realiada por [Joan Prieto](https://github.com/joanPri) y [Ricardo Martinez](https://github.com/joanPri), ambos pertenecen al aula 2 de _Tipología y ciclo de vida de los datos_.


## Explicación
En este proyecto se podran observar dos scripts diferentes, en cada uno de ellos se han implementado las metodologias actuales de scrapping. En el script llamado **"main.py"**, se ha llevado a cabo una recopilacion de los datos de la página web seleccionada mediante peticiones Request, estas permiten hacer paticiones HTTP y obtener mediante BeautifulSoup el contenido de una página web para posteriormente ser procesado.

Por otro lado se puedo ver otro script denominado **"scrapper.py"**, este aplica la metodologia de Selenium para obtener los datos de la página web. Selenium nos permite una interacción más completa con la página web, pudiendo ejecutar scripts de la própia página web, así como ejecutar clicks sobre botones. Tambien basado en peticiones HTTP, se apoya en un driver (en función del explorador será diferente) para ello. Este driver hace de conexión con el explorador, permitiendo testear la página web.

*Nota: Los scripts son totalmente independientes, no hace falta ejecutarlos a la vez.*

## Instalación

Para ejecutar el script "main.py" (en python) es necesaria la instalación de diversas bibliotecas:

```
import pandas as pd
from bs4 import BeautifulSoup
import requests
import lxml
import re
import time

```

Para ejecutar el script "scrapper.py" (en python) es necesaria la instalación de diversas bibliotecas:

```
import selenium
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pandas as pd
```

Para usar selenium se necesita un driver que haga de interficie con el navegador, estos drivers estan en la carpeta Drivers, en este proyecto el driver està vinculado con el navegador firefox, pero ofrecemos tanto chome como microsoft excel cambiando una linea de codigo y aplicando el navegador con su webpack correspondiente.
Hemos adjuntado los drivers en el proyecto (carpeta "drivers").

## Entorno de desarrollo
Para llevar a cabo el proyecto nos hemos ayudado de la distribucion de Anaconda. Esta nos facilita el paquete Python para poder trabajar con dicho lenguaje de progrmación.
Por lo tanto es necesario disponer de Anaconda instalado en Windows10 (se opta por este sistema operativo por ser de fácil manejo y de amplia implemetnación).

## Ejecturar script (usage)
Para poder ejecutar ambos script dispuestos en este proyecto, deberemos de disponer en la misma caparpeta el Driver "geckodriver" (para el caso scrapper.py), este driver corresponde a Firefox. Es el que hemos elegido aunque se podria disponer de otro driver (en la carpeta adjunta se disponen lo drives de Edge y de Chrome) para implementar el scrapper. 
Por lo tanto desde la linea de comandados en el prompt de Anaconda, y situandonos en el directorio donde se encuentre el fichero, tenemos que:
Ejecutar los scripts de la siguiente manera:
```
scrapper.py
main.py
```
En el caso del script main.py al no poder interaccionar con los datos javascript o scripts de la página recoge una menor variedad de datos:
El script se encarga de recoger los datos de indeed y extraer los siguiente campos exportados en un dataset en csv:
- Título del trabajo - String(recoge el tag titulo de cada clickcard)
- Empresa - String (recoge el tag de la compañia anunciante)
- Descripción - String (recoge la descripción completa que se obtiene 
- Link (url)
- Localización (en este caso será Barcelona o alrededores)


En el caso del script scrapper.py al interactuar con los datos javascript y los scripts recoge una información mas diversa, aunque menor cantidad por el punto que se comenta a continuación:
- Título del trabajo - String(recoge el tag titulo de cada clickcard)
- Empresa - String (recoge el tag de la compañia anunciante)
- Descripción - String (recoge la descripción completa que se obtiene 
- Link (url)
- Localización (en este caso será Barcelona o alrededores)
- Descripcion empleo (Resumen de la oferta)
- Fecha de publicación (Cuando se publicó)
- Profile - Si la oferta es para junior, senior o indefinido (este campo lo calculamos nosotros buscando en todo el contenido si aparecen estas palabras).

Debemos comentar los siguientes puntos de interes:
- Para poder interactuar con los elementos que nos ofrecia la pagina web seleccionada empleamos Selenium.
Al emplear dicho paquete frente a Request, hemos encontrado un inconveniente y es la detección de los bots por parte de las páginas Web así como la denegación de acceso a la web por "hcaptcha". Tras investigar como intentar implementar un comportamiento mas humano a nuestro bot, (modificanod el user agent en la options del driver cuando lanzamos las peticiones, como cancelando los alert dialog que se nos muestran,etc) no hemos podido conseguir pasar del paginado número 5.
Por lo tanto obtenemos el total de los puesto de trabajo de las 4 paginas primeras.
- Por el contrario Request lleva a cabo un parseo total de todo el páginado.
- 
## Futuros pasos
Para continuar indagando en el mundo del scrapping debemos conocer en mayor medida como trabajan estos detectores de bots, asi como implementar tecnicas que recreen de manera mas correcta la interacción humana. Además seria buena idea añadir un menú o la posibilidad de añadir parametros a la ejecución del script. 

## Documentación
Si quiere consultar la descripción de la práctica, consulte la [documentación](https://github.com/joanPri/indeed-web-scrapper/tree/main/doc).

## Ejemplo de salida
Para ver como queda una exportación de las ofertas de trabajos que se extraen con el script, entra [aquí](https://github.com/joanPri/indeed-web-scrapper/blob/main/indeedScrap_selenium.csv).

## Resumen
Para concluir comentar en que dos ámbitos diferentes usariamos cada script.
a) En un caso en el cual únicamente se requiera del parseo de la página web que se renderiza de manera directa tras una petición HTTP empleariamos el script main.py y su metodología dispuest, este es más ligero que Selenium dando una mayor velocidad de procesado.
b) En caso de tener que ejecutar elementos dinámicos o scripts, así como código de javascript, nos decantariamos por Selenium a pesar del inconveniente comentado.
