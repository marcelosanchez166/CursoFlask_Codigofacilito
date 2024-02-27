#Archivo para configuracion de metodo de envio de correos

from flask_mail import Message
from flask import current_app#Importando el archivo de configuracion de nuestra aplicacion current_app hace referencia a nuestra app actual 
from flask import render_template
from threading import Thread

"""Envio de correo normal pero tarda mucho en el proceso de envio, la compra se hace rapido pero el proceso de envio de correo tarda 
def confirmacion_compra(mail,usuario,libro):#mail es la variable que nuestra aplicacion utiliza para poder gestionar el envio de correos 
    try:
        message=Message("Confirmacion de compra de libro ", #Se crea una variable apartir de la clase Message de Flask y se le pasan los siguientes valores el titulo del correo  el sender que es el que envia el correo en otra palabras el remitente y el destinatario
        sender=current_app.config["MAIL_USERNAME"], 
        recipients=['marcelosachez166@gmail.com'])
        message.html= render_template('emails/confirmacion_compra.html', usuario=usuario, libro=libro)#HAciendo el llamado de la plantilla que se enviara por correo ademas se le pasaran los valores de usuario y libro 
        mail.send(message)#La variable mail es la que enviara el correo y es la que inicializamos en el archivo __init__.py
    except Exception as ex:
        raise Exception(ex)
"""

#Envio de correo asincrona "Mas rapido que el metodo de arriba"
def confirmacion_compra(app,mail,usuario,libro):#mail es la variable que nuestra aplicacion utiliza para poder gestionar el envio de correos 
    print(usuario , "en confirmacion compra")
    try:
        message=Message("Confirmacion de compra de libro ", #Se crea una variable apartir de la clase Message de Flask y se le pasan los siguientes valores el titulo del correo  el sender que es el que envia el correo en otra palabras el remitente y el destinatario
        sender=current_app.config["MAIL_USERNAME"], 
        recipients=['marcelosanchez166@gmail.com'])
        message.html= render_template('emails/confirmacion_compra.html', usuario=usuario, libro=libro)#HAciendo el llamado de la plantilla que se enviara por correo ademas se le pasaran los valores de usuario y libro 
        thread=Thread(target=Envio_Email_Async, args=[app,mail, message]   )#Usando el metodo Thread que se importo en la parte de arriba que se ocupa para abrir hilos, Se le pasan los parametros target que es la funcion que sirve para poder enviar el correo de manera asincrona el target recibira el meto que cree abajo llamado Envio_Email_Async y ciertos argumentos en una lista  
        thread.start()
    except Exception as ex:
        raise Exception(ex)
    

def Envio_Email_Async(app, mail, message):#este metodo recibira la aplicacion para poder utilizar el contexto, la variable mail para poder enviar el correo y el mensaje
    with app.app_context(): #Con el contexto de la aplicacion para que el envio del correo se de manera asincrona usando el mismo contexto de la aplicacion en la cual llamamos a esta funcion para que este hilo forme parte del flujo natural de la aplicacion y asi evitar la demora de tiempo del proceso de envio de correo
        mail.send(message)