# AIRLINE DOCKER

## About
Este software es una prueba de concepto de una aplicacion Flask en docker.  Tiene tres paginas para 
* Crear una reservacion
* Listar los Vuelos
* Mostrar la lista de pasajeros de un vuelo.

Esta basada en la aplicacion `airline` del curso de [desarrollo web con Python y Javascript de Harvard University](https://courses.edx.org/courses/course-v1:HarvardX+CS50W+Web/course/).

## Comandos docker

El ambiente necesita dos imagenes para correr la aplicacion:  Una base de datos de postgres y una aplicacion flask.  La primera contiene los datos de los vuelos y los pasajeros, y la segunda es el servidor donde vive la aplicacion web.

 Utilice este comando para crear la imagen de base de datos postgres:
 
 ``` docker build -t postgres-flask --file Dockerfile.postgres . ```

 Utilice este comando para levantar la base de datos postgres:
 
 ``` docker run --name postgres-flask -p5432:5432 -e POSTGRES_USER=root -e POSTGRES_PASSWORD=test1234 -d postgres-flask:latest```
 
 Posteriormente este otro para construir la imagen:
 
 ```docker build -t airline .```
 
 Finalmente, este comando levantara la aplicacion en el puerto 5000
 
 ```
docker run --name airline -p5000:5000 --link postgres-flask -e DATABASE_URL=postgres://root:test1234@postgres-flask/flights -
e FLASK_APP=application.py airline
```
