#Creacion de clase para la tabla TipoUsuario en la cual podriamos realizar CRUD de los tipos de usuarios que puede haber en la app 
class TipoUsuario():
    def __init__(self,id, nombre):
        self.id=id
        self.nombre=nombre