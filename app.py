
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({
        "message": "Docker Networking Lab",
        "status": "running",
        "network": "my-bridge-net",
        "services": ["Flask", "MySQL", "Redis"]
    })


@app.route("/about", methods=["GET"])
def about():
    return jsonify({
        "name": "Simple REST API",
        "version": "1.0",
        "description": "This is a simple REST API built with Flask."
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False)
