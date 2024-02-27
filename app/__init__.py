from flask import Flask, render_template,request, redirect, url_for, flash, jsonify
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect #libreria para poder crear tokens esta se instalo con pip y generaremos tokens personalizados con la SECRET_KEY que creamos en el archivo config.py
from flask_login import LoginManager,login_user,logout_user, login_required, current_user #Importando los modulos logout_user, LoginManager, login_user y login_required para gestionar el login de la aplicacion las sesiones y el logout de los usuarios y el @login_required es para que no se pueda acceder a las rutas solo con colocarlas en la en la url el current_user es el metodo que nos sirve para ver si el usuario esta logueado
from flask_mail import Mail


from .consts import *
from .emails import confirmacion_compra#importando el metodo confirmacion_compra del archivo emails.py


from .models.modelolibro import ModeloLibro #Importando la clase ModeloLibro del paquete modelolibro.py
from .models.entities.usuario import Usuario
from .models.modelousuario import ModeloUsuario
from .models.entities.libro import Libro
from .models.entities.compra import Compra
from .models.modelocompra import ModeloCompra


from werkzeug.security import check_password_hash, generate_password_hash

app=Flask(__name__)
login_manager_app=LoginManager(app)#creamos una variable que hara uso de LoginManager y le pasamos la variable app que hace referencia a nuestra propia app, LoginManager sirve para poder crear un administrador para nuestra app 
mail=Mail()

print(mail, "Instancia de mail")


#Existe un ataque a formularios que se llama CSRF(Cross-site Request Forgery) (Solicitud de Falsificacion entre sitios) 
#que se enfoca en realizar peticiones al formulario que no son de nuestro sitio
"""Para evitar estos ataques podemos usar una herramienta que nos da Flask que se llama WTF que se instala con pip install Flask-WTF, con esto realizaremos es que cada 
vez que tengamos un formulario vamos a crear un token para identificarnos como los que estamos realizando las peticiones a nuestra aplicacion"""
csrf=CSRFProtect()

db=MySQL(app)#Declaro una variable que instanciara el conector de mysql y se le pasa la variable app que se creo para instanciar Flask(__name__) 
#sobre la cual va a tener efecto para que se pueda conectar a mysql y se usara realizar conexiones atravez de los modelos, los modelos seran unas clases que se van a crear nos 
#permitira tener metodos para hacer CRUD registro de sesion etc que vamos a necesitar para conectarnos a una base

@login_manager_app.user_loader #Se debe implementar para que se gestionen correctamente las sesiones atravez de la libreria flask_login Si no creamos el decorador login_manager_app dara este error Exception: Missing user_loader or request_loader. Refer to http://flask-login.readthedocs.io/#how-it-works for more info. cuando estemos usando login_user y Login_Manager de flask
def load_user(id):#Se crear la funcion load_user y se le pasa el id que vamos a cargar del usuario
    print(id, "Id desde la funcion load_user")
    return ModeloUsuario.obtener_por_id(db,id) #retornamos el metodo obtener_por_id de la clase ModeloUsuario del archivo modelousuario.py y se le pasaran dos valores la conexion a la base y el id que vamos a cargar del usuario



#Funcion de prueba para encriptar password que le pase en la url
# @app.route("/password/<password>")
# def password(password):
#     passw=generate_password_hash(password)
#     return passw


@app.route("/login", methods=["GET", "POST"] )#En las rutas por defecto el metodo permitido es GET, Por eso hay que declarar los demas metodos
def login():
    # print(request.method)#Forma para ver porque metodo se estan enviando los datos 
    if request.method=="POST":#En esta condicion evalua si el metodo asigando en el formulacion de logue sus datos se estan enviando por el metodo GET o por POST
        #if request.form["Usuario"]=="admin" and request.form["password"]=="123456":
        #return render_template("index.html")#El render_template tambien sirve para dirigir a otra plantilla pero cuando pero para este caso es mejor el redirect ya que funciona como redireccionamiento
        usuario=Usuario(None,request.form['usuario'],request.form['password'],None) #Creamos la variable usuario para poder instanciar la clase Usuario que recibira los paramtros del formulario que esta en el archivo usuario.py el id del usuario y el tipo de usuario lo declaramos como None porque no nos siver dado que solo necesitamos las pass y el usuario
        #print(type(usuario))
        usuario_logueado=ModeloUsuario.login(db,usuario) #esta variable instanciara la clase ModeloUsuario y tendra lo que retorne modelousuario.py en el metodo de clase login que se encuentra en dicho archivo ademas se le pasara la conexion de la base y la variable usuario que tendra el usuario que recibamos como parametro en el formulario
        print(usuario_logueado)
        if usuario_logueado != None:#si la varibale usuario_logueado es diferente None
            login_user(usuario_logueado)#Utilizando el modulo login_user de flask para poder loguear al usuario que se devuelve como inicio de sesion exitoso sirve para ver la sesion del usuario que se ha logueado
            flash(MENSAJE_BIENVENIDA,'success')#flash es un metodo de flask que sirve para enviar msjs en este caso lo ocuparemos para indicar cuando las credenciales son invalidas, hay que importar flash de Flask, pero para que se muestren dichos msjs hay que indicar que se muestren en la plantilla correspondiente en este caso la plantilla login.html se le pasa otro parametro para identificar la categoria como segundo parametro el valor que success para indicar que todo ha ido bien 
            return  redirect(url_for("index"))#El redirect sirve para dirigir al usuario a otra plantilla
        else:
            flash(LOGIN_CREDENCIALESINVALIDAS,'warning')#flash es un metodo de flask que sirve para enviar msjs en este caso lo ocuparemos para indicar cuando las credenciales son invalidas, hay que importar flash de Flask, pero para que se muestren dichos msjs hay que indicar que se muestren en la plantilla correspondiente en este caso la plantilla login.html, ademas le paso otro parametro para identificar la categoria del msj 
            return  render_template("auth/login.html")
        #print(request.form["Usuario"])#Imprimiendo lo que se envia en los inputs de la plantilla login 
        #print(request.form["password"])#Imprimiendo lo que se envia en los inputs de la plantilla login 
        #return render_template("index.html")#Luego de que se reciban los parametros por el metodo POST y se han valido se redigira hacia otra plantilla en este caso a index.html
    else:
        return render_template("auth/login.html")



@app.route("/libros")
@login_required#DEcorador para que no se pueda acceder a las rutas colocandolas en la url para que solo se puedan acceder a ellas solo si el usuario esta logueado
def listar_libros():
    try:
        #Creamos una variable libros donde se guardara lo que nos devuelve el metodo de clase ListarLibro pero debemos importar el paquete modelolibro.py
        libros=ModeloLibro.ListarLibro(db)#En la variable libros estamos instanciando la clase ModeloLibro y su metodo de clase ListarLibro, ListarLibro este se encarga de realizar la conexion y la devolucion de los libros listados ademas se le debe pasar la variable db que recibe el metodo ListarLibro
        #Creamos un diccionario que recibira como valor la variable libros y se hace mediante diccionario o tuplas ya que son las que pueden ser interpretadas por el navegador y flask
        data={
            'titulo':'Listado de libros',
            'libros':libros
        }
        return render_template('listado_libros.html', data=data)#Retornamos un el render_template listar_libros.html y le creamos una variable data para pasarle la variable del diccionario que contiene los libros
    except Exception as ex:
        return render_template("errores/error.html", mensaje=format(ex))


@app.route('/comprarLibro', methods=['POST'])
@login_required
def comprarLibro():
    data_request = request.get_json()#variable para recibir la data en formato JSON, dicha variable es de tipo diccionario
    print(data_request)
    #print(type(data_request))
    data={}
    try:
        #libro = Libro(data_request['isbn'],None,None,None,None) #Se creara una instancia de la clase Libro del archivo libro.py y se le pasa el primer valor que es el isbn que se recibe en el diccionario de la variable data_request y los demas valores que recibe o espera el constructor __init__ de la clase Libro se le pasaran como None porque no los necesitamos
        libro=ModeloLibro.Leer_Libro(db,data_request['isbn'])#Como se comento la linea de arriba ya que la instancia de La Clase Libro se realizo en el archivo ModeloLibro.py en el metodo Leer_Libro, por eso en esta linea se instancia dicho metodo y se le pasan dos valores la conexion a la base y el isbn obtenido del consumo de la fetchapi la cual es obetenido mediante formato JSON 
        compra = Compra(None, libro, current_user)#Creando varible que instanciara la clase compra del archivo compra.py dicha clase necesita 4 parametros que son uuid,libro_isbn,usuario_id,fecha, pero el uuid se pasara como None porque no lo sabemos dado que el proceso es para poder crear una compra, el segundo y tercer parametro si se pasaran que son libro_isbn(La variable libro que se creo para instanciar la clase Libro), usuario_id(current_user que es el usuario actual)
        modelo_compra = ModeloCompra.registrar_compra(db, compra)#el archivo ModeloCompra aun no existe y no tiene el metodo registrar_compra, pero se crea la instancia y se le pasan como atributos la conexion a la base y la variable de instancia compra que se creo mas arriba
        data['exito'] = modelo_compra #como la instancia de la clase ModeloCompra con su metodo registrar_compra del archivo modelocompra.py devuelve un valor booleano True o False por eso se le pasa al diccionario data 
        #confirmacion_compra(mail, current_user, libro)#Este es un envio de correo sincrono  Se le pasan los parametros que necesita la variable mail que se encarga del envio de los correos, el current_user que es el usuario actual y que realizo la compra, y el libro que es instanciado un par de lineas mas arriba 
        confirmacion_compra(app,mail, current_user, libro)#Este es un envio de correo asincrono 
    except Exception as ex:
        data['mensaje'] = format(ex)
        data['exito'] = False
    return jsonify(data)#La respuesta la vamos a retornar en formato JSON y sera retornada en formato JSON por que la respuesta va a ser recibida  por la peticion response que se encuentra en el archivo listado_libro.js ya que luego esa peticion esta en formato JSON 


@app.route("/")
@login_required
def index():
    if current_user.is_authenticated:#PReguntamos si el usuario esta autenticado si esta autenticado lo redirije haci la plantilla index.html
        if current_user.tipo_usuario.id == 1:
            try:
                lista_Libros_vendidos =  ModeloLibro.Listar_Libros_Vendidos(db)
                data={
                    'titulo':'Libros Vendidos',
                    'lista_Libros_vendidos':lista_Libros_vendidos
                }
                return render_template("index.html", data=data)
            except Exception as ex:
                return render_template("errores/error.html", mensaje=format(ex))
        else:
            try:
                Lista_Compras_libros=ModeloCompra.listar_compras_usuario(db,current_user)#Se crea una instancia de la clase ModeloCompra con para poder obtener el metodo de clase listar_compras_usuario al cual le pasaremos dos valor la conexion a la base y el usuario actual 
                data={
                    'titulo':'Mis compras',
                    'Lista_Compras_libros':Lista_Compras_libros
                }
                return render_template("index.html", data=data)
            except Exception as ex:
                return render_template("errores/error.html", mensaje=format(ex))
    else:#Si no esta logueado el usuario lo rederijira hacia la ruta login para que se pueda loguear
        return redirect(url_for('login'))



@app.route("/logout")
def logout():
    logout_user()
    flash(LOGOUT, 'success')#flash es un metodo de flask que sirve para enviar msjs en este caso lo ocuparemos para indicar cuando las credenciales son invalidas, hay que importar flash de Flask, pero para que se muestren dichos msjs hay que indicar que se muestren en la plantilla correspondiente en este caso la plantilla login.html se le pasa otro parametro para identificar la categoria como segundo parametro el valor que success para indicar que todo ha ido bien 
    return redirect(url_for("login"))


def pagina_no_encontrada(error):
    #render_template sirve para poder renderizar una plantilla .html
    return render_template("errores/404.html"),404 #Flask siempre va a buscar las plantillas en la carpeta templates por lo que solo es necesario indicar la subcarpeta dentro de templates
#y la plantilla en este caso 404.hmtl y colocamos una coma para concatenar el codigo de error que queremos mostrar

def pagina_no_autorizada(error):
    return redirect(url_for('login'))#La diferencia entre un render_template y un redirect es que el redirect se ocupa para redirijir hacia una ruta y el render_template hacia una plantilla html


def inicializar_app(config):#Esta funcion retornara la variable que sostiene la instancias de flask, esta recibiendo la configuracion como parametro
    app.config.from_object(config)#La app va a recibir una configuracion y va ser obtenida de un objeto y recibira la configuracion como se observa en el codigo app.config.from_object(config)
    csrf.init_app(app)#Inicializaciamos nuetra instancia y le pasamos nuestra instancia de la app a la instancia que creamos del generador de tokens que nos ayudara con la seguridad de nuestra aplicacion y formularios
    #Registrar un manejador de errores
    mail.init_app(app)#Inicializando el servidor de correos en la aplicacion
    app.register_error_handler(404, pagina_no_encontrada)#Le estoy indicado al manejador de errores que la vista que va a lanzar es pagina_no_encontrada que llama a 404.html
    app.register_error_handler(401, pagina_no_autorizada)
    return app