from flask import Flask, request, jsonify
import numpy as np
from conf import supabase  # Asume que conf.py está en el mismo directorio y configurado

app = Flask(__name__)

@app.route('/estadisticas/equipo', methods=['GET'])
def estadisticas_equipo():
    nombre_equipo = request.args.get('nombre')
    if not nombre_equipo:
        return jsonify({'error': 'Falta el nombre del equipo'}), 400

    try:
        response = supabase.table('EstadisticasEquipos').select('*').eq('nombre_equipo', nombre_equipo).execute()

        if response.error or not response.data:
            return jsonify({'error': 'Equipo no encontrado'}), 404

        estadisticas_equipo = response.data[0]  # Asume que hay una fila por equipo

        # Calcular estadísticas globales
        total_partidos = estadisticas_equipo['partidos_ganados'] + estadisticas_equipo['partidos_empatados'] + estadisticas_equipo['partidos_perdidos']

        if total_partidos == 0:
            estadisticas = {
                "porcentaje_partidos_ganados": 0,
                "porcentaje_partidos_empatados": 0,
                "porcentaje_partidos_perdidos": 0,
                "puntos_totales": estadisticas_equipo['puntos_totales'],
            }
        else:
            porcentajes = np.array([estadisticas_equipo['partidos_ganados'], estadisticas_equipo['partidos_empatados'], estadisticas_equipo['partidos_perdidos']]) / total_partidos * 100
            estadisticas = {
                "porcentaje_partidos_ganados": round(porcentajes[0], 2),
                "porcentaje_partidos_empatados": round(porcentajes[1], 2),
                "porcentaje_partidos_perdidos": round(porcentajes[2], 2),
                "puntos_totales": estadisticas_equipo['puntos_totales'],
            }

        return jsonify(estadisticas)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Corre en un puerto diferente al del servicio de registro
