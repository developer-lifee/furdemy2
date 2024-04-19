from flask import Flask, request, redirect, url_for, render_template, jsonify
from conf import supabase  # Asegúrate de que conf.py esté en el mismo directorio y configurado

app = Flask(__name__)

@app.route('/registrar_datos', methods=['GET', 'POST'])
def registrar_datos():
    if request.method == 'POST':
        nombre_equipo = request.form.get('nombre_equipo')
        partidos_ganados = request.form.get('partidos_ganados', '0')
        partidos_empatados = request.form.get('partidos_empatados', '0')
        partidos_perdidos = request.form.get('partidos_perdidos', '0')
        puntos_totales = request.form.get('puntos_totales', '0')

        # Buscar ID del equipo basado en el nombre del equipo
        response = supabase.table('Equipos').select('id').eq('nombre', nombre_equipo).execute()
        if response.error or not response.data:
            return render_template('registrar_datos.html', mensaje_error=f"Equipo '{nombre_equipo}' no encontrado")

        equipo_id = response.data[0]['id']

        # Actualizar estadísticas del equipo en Supabase
        response = supabase.table('EstadisticasEquipos').update({
            'partidos_ganados': partidos_ganados,
            'partidos_empatados': partidos_empatados,
            'partidos_perdidos': partidos_perdidos,
            'puntos_totales': puntos_totales
        }).eq('equipo_id', equipo_id).execute()

        if response.error:
            return render_template('registrar_datos.html', mensaje_error="Error al actualizar estadísticas del equipo")

        # En este punto, deberías actualizar las estadísticas de los jugadores individualmente.
        # Esto podría implicar un formulario en tu frontend para modificar estadísticas de jugadores específicos.

        return redirect(url_for('principal'))

    # Si es una petición GET, obtener la lista de equipos para el formulario
    response = supabase.table('Equipos').select('nombre').execute()
    equipos = response.data if response.data else []

    return render_template('registrar_datos.html', equipos=equipos)

if __name__ == '__main__':
    app.run(debug=True, port=5005)
