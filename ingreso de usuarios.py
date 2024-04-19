from flask import Flask, request, jsonify, redirect, url_for, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators
from werkzeug.security import generate_password_hash, check_password_hash
from conf import supabase  # Asegúrate de que conf.py esté en el mismo directorio

app = Flask(__name__)
app.config['SECRET_KEY'] = 'una_llave_secreta_muy_segura'

# Definición del formulario de registro ya existente...

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        # Realizar la consulta en Supabase para buscar el usuario por email
        response = supabase.table('usuarios').select('*').eq('email', email).execute()

        # Verificar si hay errores o el usuario no existe
        if response.error or not response.data:
            return jsonify({'error': 'Credenciales incorrectas'}), 401
        
        usuario = response.data[0]  # Asume que el email es único y solo obtiene el primer resultado

        # Verificar la contraseña (utilizando hash)
        if check_password_hash(usuario['password'], password):
            # Aquí deberías establecer alguna forma de sesión o token de autenticación
            return jsonify({'message': 'Inicio de sesión exitoso'}), 200
        else:
            return jsonify({'error': 'Credenciales incorrectas'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Definición del endpoint de registro ya existente...

if __name__ == '__main__':
    app.run(debug=True, port=5007)
