#Creacion de clase para la tabla Libro en la cual podriamos realizar CRUD de los tipos de usuarios que puede haber en la app 
class Libro():
    def __init__(self, isbn, titulo, autor_id, yearedicion, precio):
        self.isbn = isbn
        self.titulo = titulo
        self.autor_id = autor_id
        self.yearedicion = yearedicion    
        self.precio = precio
        self.unidades_vendidas =0 #Este campo no existe en la tabla libros por lo que se define para poder mostrar la cantidad de libros vendidos 