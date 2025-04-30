from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "API funcionando desde IBM Cloud"})

@app.route("/datos", methods=["POST"])
def recibir_datos():
    data = request.json
    print("Datos recibidos:", data)
    return jsonify({"status": "ok", "data": data})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
