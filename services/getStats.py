from flask import Flask, request, jsonify, render_template, redirect, url_for
from supabase import create_client
import conf  # Importa las credenciales de Supabase desde el archivo conf.py

# Configura la aplicación Flask
app = Flask(__name__)

# Crea un cliente Supabase usando las credenciales
supabase = create_client(conf.url, conf.key)

# Define las rutas del microservicio

@app.route('/obtener_info_jugadores', methods=['POST'])
def obtener_info_jugadores():
    nombre_equipo = request.json.get('nombre_equipo')

    # Realiza una consulta a la tabla de equipos en Supabase
    response = supabase.from_('equipos').select('jugadores').eq('nombre_equipo', nombre_equipo).execute()

    # Verifica si se encontró el equipo
    if response['status'] == 200 and response['count'] > 0:
        equipo_seleccionado = response['data'][0]
        jugadores = equipo_seleccionado['jugadores']
        return jsonify({'jugadores': jugadores})
    else:
        return jsonify({'error': 'Equipo no encontrado en la base de datos'})

@app.route('/estadisticas_equipos', methods=['GET', 'POST'])
def estadisticas_equipos():
    # Realiza una consulta a la tabla de equipos en Supabase
    response = supabase.from_('equipos').select('*').execute()

    # Verifica si se pudo obtener la lista de equipos
    if response['status'] == 200 and response['count'] > 0:
        equipos_data = response['data']
    else:
        equipos_data = []

    selected_equipo = None
    estadisticas = None
    logo_url = None  # Nueva variable para almacenar la URL del logo

    if request.method == 'POST':
        selected_equipo = request.form.get('equipo')

        equipo_seleccionado = next((equipo for equipo in equipos_data if equipo["nombre_equipo"] == selected_equipo), None)

        if equipo_seleccionado:
            # Calcula las estadísticas globales
            estadisticas_globales = calcular_estadisticas_globales(equipo_seleccionado)
            estadisticas_jugadores = calcular_estadisticas_jugadores(equipo_seleccionado['jugadores'])

            estadisticas = {
                **estadisticas_globales,
                **estadisticas_jugadores,
            }

            logo_url = equipo_seleccionado.get("logo")  # Obtén la URL del logo del equipo seleccionado

    return render_template('estadisticas_equipos.html', equipos=equipos_data, selected_equipo=selected_equipo, estadisticas=estadisticas, logo_url=logo_url)

@app.route('/obtener_estadisticas_json', methods=['POST'])
def obtener_estadisticas_json():
    nombre_equipo = request.json.get('nombre_equipo')

    # Realiza una consulta a la tabla de equipos en Supabase
    response = supabase.from_('equipos').select('*').eq('nombre_equipo', nombre_equipo).execute()

    # Verifica si se encontró el equipo
    if response['status'] == 200 and response['count'] > 0:
        equipo_seleccionado = response['data'][0]
        estadisticas_globales = calcular_estadisticas_globales(equipo_seleccionado)
        return jsonify(estadisticas_globales)
    else:
        return jsonify({'error': 'Equipo no encontrado en la base de datos'})

@app.route('/cerrar_sesion')
def cerrar_sesion():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5006)
