# pip install flask-script 
#se instala ese paquete para poder gestionar de mejor manera la instancia del servidor de tal forma poder colocar en este archivo las configuraciones del servidor 

#Se importa el manager de flask_script para poder gestionar las configs del server
from flask_script import Manager,Server


#Importando la funcion inicializar_app que esta en la carpeta app 
from app import inicializar_app

#Importando el diccionario que esta en el archivo config.py
from config import config

#crear una variable que obtendra el valor development del diccionario config
configuracion=config["development"]#La variable configuracion se le pasara a la instancia de inicializar app()

app=inicializar_app(configuracion)#Instancio la funcion inicializar app de la carpeta app
manager=Manager(app)#Se crea un manejador y se le pasa la variable donde se guarda la instancia de inicializar_app como parametro

manager.add_command('runserver', Server(host='0.0.0.0', port=5000))#Sobreescribiendo la configuracion del servidor para no ejecutar el comando runserver cuando ejecuto el archivo, Hay que importar Server que esta en flask_script

if __name__ == '__main__':
    manager.run()
    #Para poder ejecutar la app debo ejecutar el siguiente comando desde la terminal python manage.py runserver


#Para este error from flask._compat import text_type ModuleNotFoundError: No module named 'flask._compat', Lo que hice para solverntarlo es dirigirme a la carpeta env del entorno virtual
#Abrir la carpeta lib y buscar la carpeta flask_script en la cual estara el archivo __init__.py y alli buscar la linea que da error y cambiar por from flask_script._compat import text_type