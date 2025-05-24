from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# Funci�n para crear una nueva conexi�n en cada solicitud
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="pi2090",
        database="Ceres",
    )

# Desactivar cach� en las respuestas
@app.after_request
def no_cache(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

# GET plantas
@app.route('/api/planta', methods=['GET'])
def obtener_plantas():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM plantas")
    datos = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(datos)

# POST plantas
@app.route('/api/planta', methods=['POST'])
def guardar_planta():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO plantas (nombre, valor) VALUES (%s, %s)",
        (data['nombre'], data['valor'])
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Planta guardada con �xito'})

# GET par�metros
@app.route('/api/parametros', methods=['GET'])
def obtener_parametros():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM parametros")
    datos = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(datos)

# GET mediciones
@app.route('/api/mediciones', methods=['GET'])
def obtener_mediciones():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM mediciones")
    datos = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(datos)

# GET alertas no resueltas
@app.route('/api/alertas', methods=['GET'])
def obtener_alertas():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM alertas WHERE resuelta = 0")
    datos = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(datos)

# Ejecutar servidor
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
