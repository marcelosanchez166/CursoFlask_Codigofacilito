#Archivo de configuracion para el proyecto

from decouple import config

class Config:#Clase que servira para tener la clave secreta que se pondra mas adelante en una instruccion
    SECRET_KEY="TWVsaW9kYXMxNTA2JCQ="#Esta es la clave secreta que la app va utilizar debe estar encriptada y servira para poder crear tokens personalizados para cada formulario y para cada peticion que se realice 


class DevelopmentConfig(Config):#clase que hereda de la clase Config y que activara el modo debug en true para que los cambios los tome en automatico el server
    DEBUG=True
    MYSQL_HOST="localhost"
    MYSQL_USER="root"
    MYSQL_PASSWORD="Meliodas1506"
    MYSQL_DB="tienda"
#Variables de entorno para la configuracion de envio de correos mediante google
    MAIL_SERVER="smtp.googlemail.com"#Simple Mail Transfer Protocol
    MAIL_PORT=587 #Puerto de google TLS
    MAIL_USE_TLS=True
    MAIL_USERNAME="marcelosanchez166@gmail.com"
    MAIL_PASSWORD=config("MAIL_PASSWORD")#Usando el metodo config de la libreria decouple para no poner la password como tal a nivel de codigo si no que se creara un archivo llamado .env para poner ese tipo de variables 
    print(MAIL_PASSWORD)

config={
    "development":DevelopmentConfig,
    "default": DevelopmentConfig
}