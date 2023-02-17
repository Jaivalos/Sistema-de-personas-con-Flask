from flask import Flask
from flask import render_template
from flaskext.mysql import MySQL

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

    sql = "INSERT INTO `empleados` (`id`, `nombre`, `correo`, `foto`) VALUES (NULL, 'Javier Avalos', 'javalos18j2@gmail.com', 'foto.png');"
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()

    return render_template('empleados/index.html')

@app.route('/create')
def create():
    return render_template('empleados/create.html')

if __name__ == '__main__':
    app.run(debug = True)