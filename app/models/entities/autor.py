#Creacion de clase para la tabla Autor en la cual podriamos realizar CRUD de los tipos de usuarios que puede haber en la app 
class Autor():
    def __init__(self,id,apellidos,nombres,fecha_nacimiento=None):
        self.id=id
        self.apellidos=apellidos
        self.nombres=nombres
        self.fecha_nacimiento=fecha_nacimiento    
    
    def Nombre_Completo(self):
        nombre_completo="{0}, {1}"#Esta variable guardara los valores de apellidos y nombres
        return nombre_completo.format(self.apellidos,self.nombres)