from .entities.compra import Compra
from .entities.libro import Libro

class ModeloCompra():
    @classmethod#Convirtiendo el metodo en un metodo de clase
    def registrar_compra(self, db, compra):#Este metodo ademas de resivir el self, el atributo db de la conexion a la base y la instancia de la clase Compra del archivo compra.py
        try:
            cursor = db.connection.cursor()
            sql="""INSERT INTO compra (uuid, libro_isbn, usuario_id) 
                    VALUES (uuid(), '{}', '{}')""".format(compra.libro_isbn.isbn, compra.usuario_id.id)#Los valores que se ingresaran es la funcion uuid(), el atributo libro_isbn de la clase Compra + el atributo isbn de la clase Libro la cual quedaria asi compra.libro_isbn.isbn y el atributo usuario_id de la clase Compra y el atributo id de la clase Usuario la cual quedaria compra.usuario_id.id
            cursor.execute(sql)
            db.connection.commit()
            return True
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def listar_compras_usuario(self, db, usuario):
        try:
            cursor = db.connection.cursor()
            sql="""SELECT COM.fecha, LIB.isbn, LIB.titulo, LIB.precio 
                    FROM compra COM JOIN libro LIB ON COM.libro_isbn = LIB.isbn 
                    WHERE COM.usuario_id  = {}""".format(usuario.id)#Los valores que se ingresaran es la funcion uuid(), el atributo libro_isbn de la clase Compra + el atributo isbn de la clase Libro la cual quedaria asi compra.libro_isbn.isbn y el atributo usuario_id de la clase Compra y el atributo id de la clase Usuario la cual quedaria compra.usuario_id.id
            cursor.execute(sql)
            data=cursor.fetchall()
            print(data)
            Lista_Compras_libros=[]
            for row in data:
                lib = Libro(row[1], row[2],None, None, row[3])
                com = Compra(None, lib, usuario, row[0])
                Lista_Compras_libros.append(com)
            #print(Lista_Compras_libros)
            return Lista_Compras_libros
        except Exception as ex:
            raise Exception(ex)