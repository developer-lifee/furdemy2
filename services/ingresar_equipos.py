from flask import Flask, request, redirect, url_for, render_template, jsonify
from conf import supabase  # Asegúrate de que conf.py esté en el mismo directorio y configurado

app = Flask(__name__)
app.config['SECRET_KEY'] = 'una_llave_secreta_muy_segura'

@app.route('/principal')
def principal():
    try:
        response = supabase.table('Equipos').select('*').execute()
        if response.error:
            equipos = []
        else:
            equipos = response.data
    except Exception as e:
        print(f"Error al cargar equipos: {e}")
        equipos = []
    return render_template('principal.html', equipos=equipos)

@app.route('/ingresar_equipos', methods=['GET', 'POST'])
def ingresar_equipos():
    if request.method == 'POST':
        nombre_equipo = request.form.get('nombre_equipo')
        logo_ruta = request.form.get('logo_ruta')

        if not nombre_equipo or not logo_ruta:
            return render_template('ingresar_equipos.html', mensaje_error="Todos los campos son obligatorios")

        try:
            response = supabase.table('Equipos').select('nombre').eq('nombre', nombre_equipo).execute()
            if response.data:
                return render_template('ingresar_equipos.html', mensaje_error="El equipo ya está ingresado")
            
            response = supabase.table('Equipos').insert({
                'nombre': nombre_equipo, 'logo': logo_ruta
            }).execute()
            
            if response.error:
                raise Exception("Error al insertar el equipo")

            # Redireccionar a la página principal una vez ingresado el equipo.
            return redirect(url_for('principal'))
        except Exception as e:
            return render_template('ingresar_equipos.html', mensaje_error=str(e))

    return render_template('ingresar_equipos.html')

if __name__ == '__main__':
    app.run(debug=True, port=5004)
