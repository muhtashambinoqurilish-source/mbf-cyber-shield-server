import os
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

    if not url or not url.startswith(("http://", "https://")):
        return jsonify({"error": "URL noto‘g‘ri"}), 400

    api_key = os.environ.get("WEBRISK_API_KEY")
    if not api_key:
        return jsonify({"error": "Server API kaliti sozlanmagan"}), 500

    try:
        response = requests.get(
            "https://webrisk.googleapis.com/v1/uris:search",
            params={
                "threatTypes": [
                    "MALWARE",
                    "SOCIAL_ENGINEERING",
                    "UNWANTED_SOFTWARE"
                ],
                "uri": url,
                "key": api_key
            },
            timeout=15
        )

        result = response.json()

        if response.status_code != 200:
            return jsonify({"error": "Tekshiruv xatosi"}), 502

        if result.get("threat"):
            return jsonify({
                "safe": False,
                "message": "XAVFLI HAVOLA ANIQLANDI"
            })

        return jsonify({
            "safe": True,
            "message": "Ma'lumotlar bazasida xavf topilmadi"
        })

    except requests.RequestException:
        return jsonify({"error": "Internet bilan aloqa xatosi"}), 502
