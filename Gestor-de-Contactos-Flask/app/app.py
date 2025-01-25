from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configuración de la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Root'
app.config['MYSQL_DB'] = 'gestor_contactos'
mysql = MySQL(app)

##HOME
@app.route('/')
def index():
    return render_template('index.html')

##REGISTO
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        email = request.form.get('email')
        contraseña = request.form.get('contraseña')
        msg_1 = ""
        msg_2 = ""

        if nombre and apellido and email and contraseña:
            cursor = mysql.connection.cursor()
            cursor.execute('INSERT INTO Usuario(nombre, apellido, email, contraseña) VALUES (%s, %s, %s, %s)', 
                           (nombre, apellido, email, contraseña))
            mysql.connection.commit()
            cursor.close()

            msg_1 = "¡Registro exitoso!"

        else:
            msg_2 = "Por favor, complete todos los campos."

        return render_template('register.html', mensaje_ok=msg_1, mensaje_no=msg_2)

    return render_template('register.html')

##LOGER
@app.route("/loger", methods=['GET', 'POST'])
def loger():

    if request.method == 'POST':
        email = request.form.get('email')
        contraseña = request.form.get('contraseña')
        msg = ""

        if email and contraseña:
            cursor = mysql.connection.cursor()
            cursor.execute()



    
    return render_template('loger.html')

if __name__ == "__main__":
    app.run(debug=True)
