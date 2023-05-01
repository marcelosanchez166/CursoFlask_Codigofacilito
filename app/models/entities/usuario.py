#Creacion de clase para la tabla Usuario en la cual podriamos realizar CRUD de los tipos de usuarios que puede haber en la app 
from werkzeug.security import generate_password_hash, check_password_hash #Importando los metodos para encriptar y desencriptar las passwords, metodo para desencriptar(check_password_hash),metodo para encriptar(generate_password_hash)
from flask_login import UserMixin

class Usuario(UserMixin):#Esta clase hereda de la clase UserMixin del paquete flask_login por eso hay que importarlo ya que necesita tener el atributo is_active que tienen la clase UserMixin para las sesiones 
    def __init__(self, id, Nombre_usuario,password, tipo_usuario):
        self.id = id
        self.Nombre_usuario = Nombre_usuario
        self.password = password
        self.tipo_usuario = tipo_usuario    

    @classmethod#Convirtiendo el metodo en un metodo de clase
    def verificar_Password(self,encriptado,password):#Se creara un metodo para realizar la verificacion de las password del usuario 
        #encriptado= generate_password_hash(password)#Esta variable recibira la password y la encriptara con el metodo generate_password_hash por eso se le pasa password
        coincide=check_password_hash(encriptado,password)#Validara que la password sea igual que la del texto que recibio por eso se le pasa la variable encriptado y el valor que tiene password para ver si coinciden
        return coincide
