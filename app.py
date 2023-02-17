from flask import Flask
from flask import render_template, request, redirect
from flaskext.mysql import MySQL
from datetime import datetime
import os

app = Flask(__name__)

#Realizamos la conexion a base de datos con FLask.
mysql = MySQL()
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'javi0712'
app.config['MYSQL_DATABASE_DB'] = 'sistema'
mysql.init_app(app)

#Obtenemos la ruta de la carpeta de las imagenes
CARPETA = os.path.join('uploads')
app.config['CARPETA'] = CARPETA

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


#Editamos un dato de la BD
@app.route('/edit/<int:id>')
def edit(id):
    sql = "SELECT * FROM `empleados` WHERE id=%s;"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql, id)
    empleados = cursor.fetchall()
    conn.commit()
    return render_template('empleados/edit.html', empleados=empleados)


#Realizamos una actualización desde el Front
@app.route('/update', methods=['POST'])
def update():
    _nombre = request.form['txtNombre']
    _correo = request.form['txtCorreo']
    _foto = request.files['txtFoto']
    id = request.form['txtId']

    datos = (_nombre, _correo, id)
    sql = "UPDATE empleados SET nombre = %s, correo = %s WHERE id = %s ;"

    conn = mysql.connect()
    cursor = conn.cursor()

    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")

    if _foto.filename != "":
        nuevo_nombre_foto = tiempo + _foto.filename
        _foto.save("uploads/"+nuevo_nombre_foto)

        cursor.execute("SELECT foto FROM empleados WHERE id = %s", id)
        fila = cursor.fetchall()

        os.remove(os.path.join(app.config['CARPETA'],fila[0][0]))
        cursor.execute("UPDATE empleados SET foto = %s WHERE id = %s", (nuevo_nombre_foto,id))
        conn.commit()

    cursor.execute(sql, datos)
    conn.commit()

    return redirect('/')


#Eliminamos un dato de la BD
@app.route('/destroy/<int:id>')
def destroy(id):
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("SELECT foto FROM empleados WHERE id = %s", id)
    fila = cursor.fetchall()
    os.remove(os.path.join(app.config['CARPETA'],fila[0][0]))

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