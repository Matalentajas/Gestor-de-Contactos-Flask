from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mysqldb import MySQL
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)
app.config['MYSQL_CONNECTION_TIMEOUT'] = 300

# Clave secreta
app.secret_key = os.getenv("SECRET_KEY")

# Configuración de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Configuración de la base de datos
app.config['MYSQL_HOST'] = os.getenv("MYSQL_ADDON_HOST")
app.config['MYSQL_USER'] = os.getenv("MYSQL_ADDON_USER")
app.config['MYSQL_PASSWORD'] = os.getenv("MYSQL_ADDON_PASSWORD")
app.config['MYSQL_DB'] = os.getenv("MYSQL_ADDON_DB")
app.config['MYSQL_ADDON_PORT'] = os.getenv("MYSQL_ADDON_PORT")

# Inicializar MySQL
mysql = MySQL(app)

class User(UserMixin):
    def __init__(self, id, nombre, email):
        self.id = id
        self.nombre = nombre
        self.email = email

@login_manager.user_loader
def load_user(user_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, nombre, email FROM Usuario WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    
    if user:
        return User(user[0], user[1], user[2])
    return None

########################

##HOME
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('perfil'))
    return render_template('index.html')

##REGISTO
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        email = request.form.get('email')
        contraseña = request.form.get('contraseña')

        if not nombre or not apellido or not email or not contraseña:
            flash("Por favor, completa todos los campos.", "error")
            return redirect(url_for('register'))

        cursor = mysql.connection.cursor()

        cursor.execute("SELECT * FROM Usuario WHERE email = %s", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash("El correo electrónico ya está registrado. Intenta con otro.", "error")
            cursor.close()
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(contraseña)

        cursor.execute(
            'INSERT INTO Usuario(nombre, apellido, email, contraseña) VALUES (%s, %s, %s, %s)', 
            (nombre, apellido, email, hashed_password)
        )

        mysql.connection.commit()
        cursor.close()

        flash("¡Registro exitoso! Ya puedes iniciar sesión.", "success")
        return redirect(url_for('loger'))

    return render_template('register.html')


##LOGER
@app.route("/loger", methods=['GET', 'POST'])
def loger():
    msg = ""
    if request.method == 'POST':
        email = request.form.get('email')
        contraseña = request.form.get('contraseña')
        
        if email and contraseña:
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT id, nombre, email, contraseña FROM Usuario WHERE email = %s", (email,))
            user = cursor.fetchone()
            cursor.close()

            if user:
                if check_password_hash(user[3], contraseña):
                    user_obj = User(user[0], user[1], user[2])
                    login_user(user_obj, remember=True)
                    return redirect(url_for('perfil'))
                else:
                    msg = "Correo o contraseña incorrectos."
            else:
                msg = "Correo no encontrado."
        else:
            msg = "Por favor, completa todos los campos."

    return render_template('loger.html', mensaje=msg)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/perfil', methods=['GET', 'POST'])
@login_required
def perfil():
    mostrar = False
    mostrar_editar = False
    contactos = {}

    if request.method == 'POST':
        # Alternar entre mostrar y ocultar el formulario al darle al botón
        if 'aoform' in request.form:
            mostrar = request.form.get('mostrar') != 'True'
        elif 'guardar_contacto' in request.form:
            nombre = request.form.get('nombre')
            apellido = request.form.get('apellido')
            email = request.form.get('email')
            telefono = request.form.get('telefono')

            if nombre and apellido and email and telefono:
                cursor = mysql.connection.cursor()
                cursor.execute('INSERT INTO Contacto (nombre, apellido, email, telefono, user_id) VALUES (%s, %s, %s, %s, %s)', (nombre, apellido, email, telefono, current_user.id))
                mysql.connection.commit()
                cursor.close()
                mostrar = False

        elif "eliminar_contacto" in request.form:
            contacto_id = request.form["contacto_id"]
            cursor = mysql.connection.cursor()
            cursor.execute('DELETE FROM Contacto WHERE id = %s', (contacto_id,))
            mysql.connection.commit()
            cursor.close()

        elif "editar" in request.form:
            mostrar_editar = request.form.get('mostrar') != 'True'
            editar_id = request.form["editar_id"]
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT id, nombre, apellido, email, telefono FROM Contacto WHERE id = %s AND user_id = %s', (editar_id, current_user.id))
            contacto_tupla = cursor.fetchone()
            cursor.close()

            if contacto_tupla:
                contactos = {
                    "id": contacto_tupla[0],
                    "nombre": contacto_tupla[1],
                    "apellido": contacto_tupla[2],
                    "email": contacto_tupla[3],
                    "telefono": str(contacto_tupla[4])
                }
            else:
                contactos = {}

        elif "actualizar_contacto" in request.form:
            contacto_id = request.form["contacto_id"]
            nombre = request.form.get('nombre')
            apellido = request.form.get('apellido')
            email = request.form.get('email')
            telefono = request.form.get('telefono')

            if nombre and apellido and email and telefono:
                cursor = mysql.connection.cursor()
                cursor.execute("""UPDATE Contacto SET nombre = %s, apellido = %s, email = %s, telefono = %s WHERE id = %s AND user_id = %s""",
                               (nombre, apellido, email, telefono, contacto_id, current_user.id))
                mysql.connection.commit()
                cursor.close()
                mostrar_editar = False

    # Código que siempre se ejecuta después de manejar POST o GET
    id = current_user.id
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT id, nombre, apellido, email, telefono FROM Contacto WHERE user_id = %s', (id,))
    contacto = cursor.fetchall()
    cursor.close()

    return render_template('perfil.html', user=current_user, mostrar=mostrar, contacto=contacto, mostrar_editar=mostrar_editar, contactos=contactos)

@app.route("/test_db")
def test_db():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT DATABASE();")
        db_name = cursor.fetchone()[0]
        cursor.close()
        return f"Conexión exitosa a la base de datos: {db_name}"
    except Exception as e:
        return f"Error conectando a la base de datos: {str(e)}"

@app.errorhandler(404)
def pagina_no_encontrada(error):
    return render_template("404.html", error=error), 404
    
if __name__ == "__main__":
    app.run(debug=True)
