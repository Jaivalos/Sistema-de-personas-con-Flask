from flask import Flask
from flask import render_template, request, redirect
from flaskext.mysql import MySQL
from datetime import datetime

app = Flask(__name__)

#Realizamos la conexion a base de datos con FLask.
mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'sistema'
mysql.init_app(app)

#Indicamos el inicio de la aplicacion en el index.html
@app.route('/')
def index():

    #Obtenemos todos los empleados de la base de datos
    sql = "SELECT * FROM `empleados`;"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    empleados = cursor.fetchall()
    print(empleados)
    conn.commit()
    return render_template('empleados/index.html', empleados = empleados)

#Eliminamos un dato de la BD
@app.route('/destroy/<int:id>')
def destroy(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM empleados WHERE id=%s", id)
    conn.commit()
    return redirect('/')


#Creamos un endpoint para obtener datos de los empleados
@app.route('/create')
def create():
    return render_template('empleados/create.html')


#Creamos un endpoint para procesar los datos de la persona
@app.route('/store', methods=['POST'])
def storage():

    _nombre = request.form['txtNombre']
    _correo = request.form['txtCorreo']
    _foto = request.files['txtFoto']

    #Guardamos la fotografia con el tiempo y el nombre de la foto, con el fin de no sobreescribir
    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")
    if _foto.filename != '':
        nuevo_nombre_foto = tiempo+_foto.filename
        _foto.save("uploads/"+nuevo_nombre_foto)

    datos = (_nombre, _correo, nuevo_nombre_foto)
    sql = "INSERT INTO `empleados` (`id`, `nombre`, `correo`, `foto`) VALUES (NULL, %s, %s, %s);"
    
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, datos)
    conn.commit()
    return render_template('empleados/index.html')


if __name__ == '__main__':
    app.run(debug = True)