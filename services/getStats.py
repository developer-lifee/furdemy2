from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from supabase import create_client
import conf  # Importa las credenciales de Supabase desde el archivo conf.py

get_stats_blueprint = Blueprint('get_stats', __name__)

# Crea un cliente Supabase usando las credenciales
supabase = create_client(conf.url, conf.key)

@get_stats_blueprint.route('/obtener_info_jugadores', methods=['POST'])
def obtener_info_jugadores():
    nombre_equipo = request.json.get('nombre_equipo')
    response = supabase.from_('equipos').select('jugadores').eq('nombre_equipo', nombre_equipo).execute()
    if response['status'] == 200 and response['data']:
        jugadores = response['data'][0]['jugadores']
        return jsonify({'jugadores': jugadores})
    else:
        return jsonify({'error': 'Equipo no encontrado en la base de datos'}), 404

@get_stats_blueprint.route('/estadisticas_equipos', methods=['GET', 'POST'])
def estadisticas_equipos():
    response = supabase.from_('equipos').select('*').execute()
    equipos_data = response['data'] if response['status'] == 200 else []
    selected_equipo = None
    estadisticas = None
    logo_url = None
    if request.method == 'POST':
        selected_equipo = request.form.get('equipo')
        equipo_seleccionado = next((equipo for equipo in equipos_data if equipo["nombre"] == selected_equipo), None)
        if equipo_seleccionado:
            estadisticas_globales = calcular_estadisticas_globales(equipo_seleccionado)
            estadisticas_jugadores = calcular_estadisticas_jugadores(equipo_seleccionado['jugadores'])
            estadisticas = {**estadisticas_globales, **estadisticas_jugadores}
            logo_url = equipo_seleccionado.get("logo")
    return render_template('estadisticas_equipos.html', equipos=equipos_data, selected_equipo=selected_equipo, estadisticas=estadisticas, logo_url=logo_url)

@get_stats_blueprint.route('/obtener_estadisticas_json', methods=['POST'])
def obtener_estadisticas_json():
    nombre_equipo = request.json.get('nombre_equipo')
    response = supabase.from_('equipos').select('*').eq('nombre_equipo', nombre_equipo).execute()
    if response['status'] == 200 and response['data']:
        equipo_seleccionado = response['data'][0]
        estadisticas_globales = calcular_estadisticas_globales(equipo_seleccionado)
        return jsonify(estadisticas_globales)
    else:
        return jsonify({'error': 'Equipo no encontrado en la base de datos'}), 404

@get_stats_blueprint.route('/cerrar_sesion')
def cerrar_sesion():
    return redirect(url_for('index'))
