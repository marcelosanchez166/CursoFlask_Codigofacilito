import datetime

#Creacion de clase para la tabla Compra en la cual podriamos realizar CRUD de los tipos de usuarios que puede haber en la app 
class Compra():
    def __init__(self, uuid, libro_isbn, usuario_id, fecha=None):
        self.uuid = uuid
        self.libro_isbn = libro_isbn
        self.usuario_id = usuario_id
        self.fecha = fecha    

    #Se creara un metodo para formatear la fecha para poder presentar la fecha de compra 
    def formatted_date(self):
        return datetime.datetime.strftime(self.fecha, '%d/%m/%Y - %H:%M:%S')