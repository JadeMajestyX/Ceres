from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# Conexi�n a la base de datos (ajusta a tu configuraci�n)
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="pi2090",
    database="Ceres",
)
cursor = db.cursor(dictionary=True)

@app.route('/api/plantas', methods=['GET'])
def obtener_datos():
    cursor.execute("SELECT * FROM plantas")
    return jsonify(cursor.fetchall())

@app.route('/api/parametros', methods=['GET'])
def obtener_parametros():
    cursor.execute("SELECT * FROM parametros")
    return jsonify(cursor.fetchall())

@app.route('/api/mediciones', methods=['GET'])
def obtener_mediciones():
    cursor.execute("SELECT * FROM mediciones")
    return jsonify(cursor.fetchall())

@app.route('/api/guardar', methods=['POST'])
def guardar():
    data = request.json
    cursor.execute("INSERT INTO tu_tabla (nombre, valor) VALUES (%s, %s)", (data['nombre'], data['valor']))
    db.commit()
    return jsonify({'mensaje': 'Dato guardado con �xito'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
