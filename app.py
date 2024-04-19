from flask import Flask
from services.getStats import getStats_blueprint
from services.registro_estadisticas import registro_estadisticas_blueprint
from services.ingresar_equipos import ingresar_equipos_blueprint
from services.registro_usuarios import registro_usuarios_blueprint
from services.stats_players import stats_players_blueprint
from services.stats_service import stats_service_blueprint
from services.ingreso_usuarios import ingreso_usuarios_blueprint

app = Flask(__name__)

app.register_blueprint(getStats_blueprint, url_prefix='/getStats')
app.register_blueprint(registro_estadisticas_blueprint, url_prefix='/registroEstadisticas')
app.register_blueprint(ingresar_equipos_blueprint, url_prefix='/ingresarEquipos')
app.register_blueprint(registro_usuarios_blueprint, url_prefix='/registroUsuarios')
app.register_blueprint(stats_players_blueprint, url_prefix='/statsPlayers')
app.register_blueprint(stats_service_blueprint, url_prefix='/statsService')
app.register_blueprint(ingreso_usuarios_blueprint, url_prefix='/ingresoUsuarios')

if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Corre en el puerto 5000
