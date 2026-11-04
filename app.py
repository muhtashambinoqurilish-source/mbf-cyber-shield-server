import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "MBF CYBER SHIELD SERVER IS RUNNING"

@app.route("/check", methods=["POST"])
def check_url():
    data = request.get_json(silent=True) or {}
    url = data.get("url", "").strip()

    if not url.startswith(("http://", "https://")):
        return jsonify({
            "safe": False,
            "message": "URL manzili noto‘g‘ri"
        }), 400

    try:
        response = requests.get(
            "https://openphish.eu/api/check",
            params={"url": url},
            timeout=15
        )

        if response.status_code != 200:
            return jsonify({
                "error": f"OpenPhish API xatosi: {response.status_code}"
            }), 502

        result = response.json()
        found = result.get("found", False)

        if found:
            return jsonify({
                "safe": False,
               "message": "XAVFLI! Fishing bazasida tasdiqlangan havola."
            })

        return jsonify({
            "safe": True,
            "message": "Bazadan fishing havolasi topilmadi"
        })

    except (requests.RequestException, ValueError):
        return jsonify({
            "error": "Tekshirish xizmatiga ulanishda xatolik"
        }), 502
