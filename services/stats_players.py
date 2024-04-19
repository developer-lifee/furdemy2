from flask import Flask, request, jsonify
import numpy as np
from conf import supabase  # Asume que conf.py está en el mismo directorio y configurado

app = Flask(__name__)

@app.route('/estadisticas/jugadores', methods=['GET'])
def estadisticas_jugadores():
    nombre_equipo = request.args.get('nombre_equipo')
    if not nombre_equipo:
        return jsonify({'error': 'Falta el nombre del equipo'}), 400

    try:
        # Obtener jugadores del equipo específico
        response = supabase.table('Jugadores').select('*').eq('nombre_equipo', nombre_equipo).execute()
        if response.error or not response.data:
            return jsonify({'error': 'Jugadores no encontrados'}), 404
        
        jugadores = response.data

        if not jugadores:
            return jsonify({
                "goles_por_remate": 0,
                "tarjetas_amarillas_por_rojas": 0,
                "mejor_goleador": None,
                "jugador_mayor_riesgo": None,
            })

        datos = np.array([[jugador.get("goles", 0), jugador.get("remates_al_arco", 0),
                        jugador.get("tarjetas_amarillas", 0), jugador.get("tarjetas_rojas", 0)] for jugador in jugadores])

        sumas_totales = datos.sum(axis=0)

        goles_por_remate = sumas_totales[0] / sumas_totales[1] if sumas_totales[1] > 0 else 0
        tarjetas_amarillas_por_rojas = sumas_totales[2] / sumas_totales[3] if sumas_totales[3] > 0 else 0

        mejor_goleador_index = np.argmax(datos[:, 0])
        mejor_goleador = jugadores[mejor_goleador_index]["nombre"]

        jugador_mayor_riesgo_index = np.argmax(datos[:, 3])
        jugador_mayor_riesgo = jugadores[jugador_mayor_riesgo_index]["nombre"]

        return jsonify({
            "goles_por_remate": round(goles_por_remate, 2),
            "tarjetas_amarillas_por_rojas": round(tarjetas_amarillas_por_rojas, 2),
            "mejor_goleador": mejor_goleador,
            "jugador_mayor_riesgo": jugador_mayor_riesgo,
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5002)  # Asumiendo que deseas ejecutarlo en un puerto diferente
