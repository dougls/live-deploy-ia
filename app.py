from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Olá! Esta aplicação foi implantada com um pipeline de CI/CD com IA da FIAP, em Agosto de 2025!</h1>"

@app.route('/health')
def health_check():
    return jsonify(status="ok", message="Aplicação está saudável para cluster EKS."), 200

@app.route('/version')
def app_version():
    image_version = os.environ.get("IMAGE_VERSION", "N/A")
    return jsonify(version=image_version)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
