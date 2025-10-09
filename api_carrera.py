import dao_Carrera as dao
from flask import request
from flask import jsonify
from flask import Flask
import carrera as c 
import mysql.connector

app = Flask(__name__)

def connect_db ():
    user = "root"
    passwd = "12345678"
    cnx = dao.connect_db(user, passwd)
    return cnx
conexion = connect_db()
cursor = conexion.cursor(dictionary=True)  # Retorna resultados como diccionarios

@app.route('/')
def hola_mundo():
    return '<p>Hola  en Flask!</p>'

@app.route('/ver/carreras/', methods=['GET'])
def api_ver_carreras():
    return jsonify(dao.ver_carreras(cursor))

@app.route('/borrar/carrera/<id>', methods=['DELETE'])
def api_borrar_carreras(id):
    carrera = c.carrera(id_carrera=id)
    return jsonify(dao.borrar_carrera(cursor,carrera))

@app.route('/agregar/carrera', methods=['POST'])
def api_agregar_carrera():
    nombre = request.args.get('nombre')
    nota = request.args.get('nota')
    duracion = request.args.get('duracion')

    if not nombre:
        return jsonify({"error": "Falta el nombre de la carrera"}), 400

    try:
        nota = float(nota)
        duracion = int(duracion)
    except (TypeError, ValueError):
        return jsonify({"error": "Valores inválidos para nota o duración"}), 400

    carrera_agregar = c.carrera(nombre, "", nota, duracion)
    dao.añadir_carrera(cursor, carrera_agregar)
    conexion.commit()

    print(f"[DEBUG] Carrera añadida: {nombre} ({nota}, {duracion})")
    return jsonify({"mensaje": "Carrera agregada correctamente"})

if __name__ == "__main__":
    print("Iniciando servidor Flask en http://127.0.0.1:5000 ...")
    app.run(debug=True, port=5000)