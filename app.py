from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Load data license dari file JSON
def load_licenses():
    with open("licenses.json", "r") as f:
        return json.load(f)

# Endpoint untuk verifikasi license
@app.route("/verify", methods=["POST"])
def verify_license():
    data = request.get_json()
    username = data.get("username")
    license_key = data.get("license")
    version = data.get("version")

    licenses = load_licenses()

    for entry in licenses:
        if (
            entry["username"] == username and
            entry["license"] == license_key and
            entry["version"] == version
        ):
            return jsonify({"valid": True})

    return jsonify({"valid": False})

# Jalankan server
if __name__ == "__main__":
    print("🚀 Menjalankan server Flask di http://127.0.0.1:5000")
    app.run(debug=True)
