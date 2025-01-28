from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mysqldb import MySQL
#Importaciones para Login
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
#Importacion para generar seguridad en las contraseñas de los usuarios usando Hash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

#Clave secreta
app.secret_key = "f18440b8772ce1f74c8877a8616dc190624015e870e9ac8d868c9b42b7027a7b"
# Configuración de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Configuración de la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Root'
app.config['MYSQL_DB'] = 'gestor_contactos'
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
        return User(user[0], user[1], user[2])  # Devuelve una instancia de User
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

        # Verificación de campos vacíos
        if not nombre or not apellido or not email or not contraseña:
            flash("Por favor, complete todos los campos.", "error")
            return redirect(url_for('register'))

        cursor = mysql.connection.cursor()

        # Comprobamos si el correo ya existe en la base de datos
        cursor.execute("SELECT * FROM Usuario WHERE email = %s", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash("El correo electrónico ya está registrado. Intenta con otro.", "error")
            cursor.close()
            return redirect(url_for('register'))
        
        # Cifrar la contraseña antes de guardarla
        hashed_password = generate_password_hash(contraseña)

        # Insertar el nuevo usuario en la base de datos
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

            if user and check_password_hash(user[3], contraseña):
                user_obj = User(user[0], user[1], user[2])
                login_user(user_obj, remember=True)
                return render_template('perfil.html', user=current_user)
        
            else:
                msg = "Correo o contraseña incorrectos."
        else: msg = "Añade todos los campos"
    return render_template('loger.html', mensaje = msg)

#Funcion para cerrar sesion

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/perfil', methods=['GET', 'POST'])
@login_required
def perfil():
    mostrar = False

    if request.method == 'POST':
        # Alternar entre mostrar y ocultar el formulario al darle al boton
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
                print("Contacto guardado con éxito")
                mostrar = False
            else:
                print("Error al añadir el contacto")

    # Código que siempre se ejecuta después de manejar POST o GET
    id = current_user.id
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT nombre, apellido, email, telefono FROM contacto WHERE user_id = %s', (id,))
    contacto = cursor.fetchall()
    cursor.close()
    print(contacto)

    return render_template('perfil.html', user=current_user, mostrar=mostrar, contacto=contacto)
    
if __name__ == "__main__":
    app.run(debug=True)
