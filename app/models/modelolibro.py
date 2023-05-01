from .entities.autor import Autor #importando la clase Autor del modulo autor.py para poder instanciarlas en el metodo ListarLibro()
from .entities.libro import Libro #importando la clase Libro del modulo libro.py para poder instanciarlas en el metodo ListarLibro()

class ModeloLibro():
    @classmethod#El decorador @classmethod sirve para indicar que este metodo ListarLibro es un metodo de clase nos servira para poder crear una instancia de la clase ModeloLibro
    def ListarLibro(self,db ):#Este metodo recibira dos parametros el self, y la variable de la base para la conexion 
        try:
            
        #Creando el cursor a la conexion a la base de datos
            cursor=db.connection.cursor()
        #Se crea la variable sql para guardar lo que traiga la consulta a la tabla libros que seran ordenados de forma ascendente
        # sql="SELECT isbn, titulo, yearedicion FROM libro ORDER BY titulo ASC"
            sql= """SELECT LIB.isbn, LIB.titulo, LIB.yearedicion, LIB.precio,
                AUT.apellidos, AUT.nombres 
                FROM libro LIB JOIN autor AUT ON LIB.autor_id=AUT.id
                ORDER BY titulo ASC """#La cláusula JOIN se utiliza para unir las filas de las tablas 'libro' y 'autor' en función de una condición en 
        #la que la columna 'autor_id' en la tabla 'libro' debe coincidir con la columna 'id' en la tabla 'autor'. Esto se utiliza para combinar la información del 
        #autor en la consulta para cada libro.
        #Usamos el cursor que creamos con el metodo execute para poder ejecutar lo nos trajo el SELECT que se guardo en la variable sql
            cursor.execute(sql)
        #Creamos una variable data que sera la data resultante con el metodo fetchall nos aseguramos de convertir la data en un objeto que se pueda iterar 
            data=cursor.fetchall()
        #print(data)
        #     data={
        #         "libros":data
        #         }
        # #return "OK. Numero de libros {}".format(len(data))
        #     return render_template("listado_libros.html",data=data)
            libros=[]
            #Para no acceder al indice en la plantilla listado_libros.html como tal de cada valor en la tupla que devuelve la variable data, por eso crearemos un ciclo for
            for row in data:
                aut=Autor(0,row[4],row[5])
                #print(row[4],row[5])
                #Con esto estamos instanciada la clase Autor para poder acceder a los apellidos y a los nombres del autor, puse ,row[4],row[5] porque son las pociciones de los elementos cuando hago el SELECT
                lib=Libro(row[0],row[1],aut,row[2],row[3])#Con esto estamos instanciada la clase Libro para poder acceder a los valores isbn,titulo,autor_id,yearedicion,precio de la clase Libro, recordar que el valor autor_id pertenece a la tabla autor y por eso en la instancia despues de poner las filas row[0],row[1] pongo la variable donde instanciamos la clase Autor
                libros.append(lib)#Utilizando de la lista libros que dejamos vacia arriba le anexaremos el libro que vamos a ir recorriendo por eso le pasamos la variable que utilizamos para instanciar la clase Libro
            #print(libros[2])
            return libros
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def Leer_Libro(self, db, isbn):
        try:
            cursor=db.connection.cursor()
            sql="""SELECT isbn, titulo, yearedicion, precio
                    FROM libro WHERE isbn = {}""".format(isbn)
            cursor.execute(sql)
            data=cursor.fetchone()#Obteniendo solo el primer dato del SELECT
            #row=data[0]#Se extrae el isbn ya que es la posicion 0 de data y la guardo en row 
            libro=Libro(data[0], data[1], None, data[2], data[3])#Apartir de la variable row creo una variable libro para instanciar la Clase Libro del archivo libro.py para obtener los datos del libro 
            return libro
        except Exception as ex:
            raise Exception(ex)


    @classmethod#El decorador @classmethod sirve para indicar que este metodo ListarLibro es un metodo de clase nos servira para poder crear una instancia de la clase ModeloLibro
    def Listar_Libros_Vendidos(self, db):#Este metodo recibira dos parametros el self, y la variable de la base para la conexion 
        try:
            cursor=db.connection.cursor()#Creando el cursor a la conexion a la base de datos
            sql= """SELECT COM.libro_isbn, LIB.titulo, LIB.precio, COUNT(COM.libro_isbn) AS unidades_vendidas 
                    FROM compra COM JOIN libro LIB ON 
                    COM.libro_isbn = LIB.isbn GROUP BY COM.libro_isbn ORDER BY 4 DESC, 2 ASC"""
            cursor.execute(sql)
            data=cursor.fetchall()#Creamos una variable data que sera la data resultante con el metodo fetchall nos aseguramos de convertir la data en un objeto que se pueda iterar 
            lista_Libros_vendidos=[]
            for row in data:#Para no acceder al indice en la plantilla listado_libros.html como tal de cada valor en la tupla que devuelve la variable data, por eso crearemos un ciclo for
                lib = Libro(row[0], row[1], None, None, row[2])#Con esto estamos instanciada la clase Libro para poder acceder a los valores isbn,titulo,autor_id,yearedicion,precio de la clase Libro, recordar que el valor autor_id pertenece a la tabla autor y por eso en la instancia despues de poner las filas row[0],row[1] pongo la variable donde instanciamos la clase Autor
                lib.unidades_vendidas = int(row[3])#llamando el atirbuto Unidades_Vendidas de la clase Libro y se coloca la posion 3 ya que esa es la posicion de dicho atributo en la consulta de arriba
                lista_Libros_vendidos.append(lib)#Utilizando de la lista libros que dejamos vacia arriba le anexaremos el libro que vamos a ir recorriendo por eso le pasamos la variable que utilizamos para instanciar la clase Libro
            return lista_Libros_vendidos
        except Exception as ex:
            raise Exception(ex)

