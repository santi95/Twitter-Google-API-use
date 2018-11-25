# Explicación Tarea 7

## Santiago Muñoz Venezian; santi95

28 de Noviembre, 2017

Para que sea más facil de corregir, lo que no me funcionó fue:

    1. Solamente soporta hasta 20 paises por culpa de la interfaz grtáfica
    2. Lo mismo para la ciudades
    3. No filtra segun lo que quiere ver el usuario
    4. No me funcionó lo de la negrita en el Spreadsheet

Todo el resto funciona super bien en general

Mi tarea tiene 5 archivos python:

    1. CiudadesGet.py:
    2. CoordenadasGet.py 
    3. TwitterGet.py
    4. Config.py
    5. Main.py
        
#### CiudadesGet

Hay 3 funciones

    Tiene una función para entregarle mis credenciales
    
    La segunda es para crear la nueva Sheet en el caso de que no exista, 
    esta tiene un feo try, que es para manejar el error de cuando la sheet
    ya estaba creada. Podría pedirle las sheets actuales del Spreadhseet, 
    pero le he dedicado todo mi tiempo de este semestre a este ramo y 
    tengo que pasar el resto de mis ramos ajjaja :((((.

    La tercera función la llamo para escribir en el sheet, le entrego una 
    lista y esta función la escribe en las columnas del sheet

#### CoordenadasGet

Esta es casi un copy paste de la documentación de google maps, me retorna las
coordenadas la ciudad en el mundo.

#### TwitterGet

La primera función me retorna la lista de los 5 primeros trending topics,
perdí mucho tiempo buscando los urls, pero cuando los encontré, aprendí
realmente como usar una API.

La segunda función me retorna los últimos 20 tweets de la zona, pedida
con las coordenadas sacadas anteriormente. Retorna una lista, 
si el largo de esa lista es menor a 20, el logger lo detecta y hace el
warning.

#### Config

Tiene todas las claves necesarias para que el programa pueda autenticarse 
con las APIS pedidas. Tal como fue pedido en el enunciado

#### Main.py

Aquí es donde ocurre toda la magia del sur. 

Primero pide un link de google sheets, llama al módulo CiudadesGet y 
muestra esos paises en la interfaz. Luego de escribir el nombre del pais, 
(sorry por eso D:) te muestra las ciudades dentro de ese país. Donde tienes
que escribir la ciudad para la cual quieres saber la información.

Con el nombre de la ciudad, le pide la coordenadas a google maps mediante el
módulo de CoordenadasGet y se las entrega al Módulo TwitterGet para que 
obtenga toda la información pedida por la tarea desde Twitter. Primero
retorna los 5 Trending Topics ordenados por Tweet Volume y luego, 
muestra los 20 tweets más recientes. 

Nunca pude descubrir por qué no funcionaba el since del url de twitter.

        "/search/tweets.json?since{year}-{month}-{day}&geocode=..."

Probé de todas las posibles combinaciones y nunca me funcionó que me restrinja solo tweets de los últimos 2 días. 

Escribe todos los tweets en una HTML browser en formato HTML y al final a la
derecha tiene un botón que te abre tu navegador preferido (Internet Explorer 
obviamente) y te muestra el Sheet.

Los loggers los llamo con tweets y imprimen en la consola y en el archvio.txt
usé 2 handlers. No me resultó usar un handler para escribir el logger en los
sheets, pero lo hice igual, de una manera que no sé que tan legal era.

Entretenida la tarea, super aplicada y útil para el futuro.

Espero pasar este ramooooooo, jajajaja bueno ojalá. 

Gracias por corregir mi Tarea ojalá estés de vacaciones y suerte!!
