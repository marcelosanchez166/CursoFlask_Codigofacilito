#Este archivo servira para tener la logica del inicio de sesion
#from werkzeug.security import check_password_hash
from .entities.usuario import Usuario
from .entities.tipousuario import TipoUsuario

class ModeloUsuario():
    @classmethod#Convirtiendo el metodo login en un metodo de clase 
    def login(self,db,usuario):#este metodo recibe TRES parametros la conexion a la base y el self en referencia a la propia clase ademas del usuario que entra en el formulario
        try:
            cursor=db.connection.cursor()
            sql="""SELECT id, Nombre_usuario, password FROM usuario WHERE
                    Nombre_usuario = '{}'""".format(usuario.Nombre_usuario)#En el format se le pasa el atributo que recibe el metodo login y el atributo que recibe el construtor __init__ de la clase Usuario en el archivo usuario.py
            cursor.execute(sql)
            data=cursor.fetchone()#Usamos el metodo fecthone porque solo esperamos recibir un registro en este caso solo el usuario 
            #print(data)
            #coincide=check_password_hash(data[2],usuario.password)#Aqui validamos que la posicion dos de la tupla coincida con la la clave que se le ingresa y es encriptada ademas se le pasa el atributo usuario del metodo login y el atributo del constructor de la clase Usuario en el archivo usuario.py
            if data != None:
                coincide=Usuario.verificar_Password(data[2],usuario.password)
                if coincide:#Si la variable coincide es verdadera 
                    usuario_logueado=Usuario(data[0],data[1],None,None)#Instanciamos la clase Usuario del archivo usuario.py y solo les pasamos los argumentos de las posiciones 0 y 1 que corresponden al id y al Nombre_usuario y la password y el tipo de usuario le ponemos None para no exponer esos campos
                    return usuario_logueado
                else:
                    return None
            else:
                    return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def obtener_por_id(self,db,id):
        try:
            cursor=db.connection.cursor()
            sql="""SELECT USU.id, USU.Nombre_usuario, TIP.id, TIP.nombre
                    FROM usuario USU JOIN tipousuario TIP ON USU.tipousuario_id=TIP.id
                    WHERE USU.id = {}""".format(id)#En el format se le pasa el atributo que recibe el metodo obtener_por_id  
            cursor.execute(sql)
            data=cursor.fetchone()#Usamos el metodo fecthone porque solo esperamos recibir un registro en este caso solo el id 
            tipousuario=TipoUsuario(data[2], data[3])#creamos una instancia de la clase TipoUsuario y le pasamos las posiciones de 2 y 3 de la tupla data que son el id del tipo y el nombre del tipo
            usuario_logueado= Usuario(data[0],data[1],None,tipousuario)#Creamos una instancia de la clase Usuario y le pasamos las posiciones 0 que corresponde al id del usuario 1 de Nombre_usuario None para la clave ya que no la usaremos y la variable tipousuario que contiene las posiciones de 2 y 3 de la tupla data que son el id del tipo y el nombre del tipo
            return usuario_logueado #Este se almacena en la funcion load_user del archivo __init__.py
        except Exception as ex:
            raise Exception(ex)