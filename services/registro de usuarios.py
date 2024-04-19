from flask import Flask, request, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators
from werkzeug.security import generate_password_hash
from conf import supabase  # Asegúrate de que conf.py esté en el mismo directorio

app = Flask(__name__)
app.config['SECRET_KEY'] = 'una_llave_secreta_muy_segura'

# Define un formulario de registro usando Flask-WTF
class RegistrationForm(FlaskForm):
    name = StringField('Name', [validators.DataRequired()])
    email = StringField('Email', [validators.DataRequired(), validators.Email()])
    password = PasswordField('Password', [validators.DataRequired()])

@app.route('/register', methods=['POST'])
def register():
    form = RegistrationForm(request.form)
    if form.validate():
        name = form.name.data
        email = form.email.data
        password = generate_password_hash(form.password.data, method='sha256')

        # Intenta insertar el nuevo usuario en Supabase
        try:
            response = supabase.table('usuarios').insert({
                'nombre': name,
                'email': email,
                'password': password
            }).execute()

            if response.error:
                return jsonify({'error': 'No se pudo registrar el usuario'}), 400
            else:
                return jsonify({'message': 'Usuario registrado con éxito'}), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Datos de formulario no válidos'}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5003 )
