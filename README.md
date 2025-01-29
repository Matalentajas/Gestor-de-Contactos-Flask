Proyecto de Gestión de Contactos
Este proyecto es un ejercicio de práctica personal para gestionar contactos. A través de este sistema, los usuarios pueden agregar, editar y eliminar contactos, permitiendo almacenar información como el nombre, apellido, correo electrónico y teléfono. El proyecto está diseñado para poner en práctica el uso de Flask, MySQL y la autenticación de usuarios.

Funciones Principales
Registro y Autenticación de Usuarios
Los usuarios pueden registrarse y acceder a la aplicación para gestionar sus contactos. La autenticación está protegida mediante la librería Flask-Login.

Gestión de Contactos
Los usuarios pueden:

Añadir un nuevo contacto: Ingresando nombre, apellido, correo electrónico y teléfono.
Editar un contacto: Modificando la información de un contacto previamente añadido.
Eliminar un contacto: Eliminando un contacto de la base de datos.
Interfaz de Usuario

Un formulario de búsqueda permite a los usuarios buscar sus contactos.
Un formulario de edición facilita la actualización de los datos de contacto.
Tecnologías Usadas
Flask: Framework de Python para el desarrollo web.
MySQL: Base de datos relacional para almacenar los datos de los contactos.
Flask-Login: Librería para gestionar la sesión de usuarios.
HTML/CSS: Estructura y estilo de la interfaz web.
Instalación
Clona este repositorio:

git clone https://github.com/Matalentajas/gestion-contactos.git
Instala las dependencias:

pip install -r requirements.txt
Configura la base de datos en MySQL, asegurándote de tener una tabla Contacto con las columnas adecuadas (id, nombre, apellido, email, telefono, user_id).

Ejecuta la aplicación:

flask run

Uso
Regístrate y accede a la aplicación.
Añade, edita o elimina contactos según lo necesites.
Utiliza la interfaz para navegar entre las opciones y gestionar tus contactos.
Contribuciones
Este proyecto es parte de mi ejercicio personal de práctica. Si tienes sugerencias o mejoras, no dudes en abrir un "issue" o hacer un "pull request".

Licencia
Este proyecto está bajo la Licencia MIT.
