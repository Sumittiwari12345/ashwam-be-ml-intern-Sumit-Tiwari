from flask import Flask, jsonify, request

from .detector import analyze_text


def build_result(payload):
    text = payload.get("text", "")
    result = analyze_text(text)
    result["id"] = payload.get("id", "")
    return result


def create_app():
    app = Flask(__name__)

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    @app.get("/")
    def index():
        return jsonify(
            {
                "service": "language-detection",
                "endpoints": {
                    "health": "/health",
                    "detect": "/detect",
                    "detect_batch": "/detect_batch",
                },
            }
        )

    @app.post("/detect")
    def detect():
        payload = request.get_json(silent=True)
        if payload is None:
            return jsonify({"error": "Expected JSON body"}), 400
        if not isinstance(payload, dict):
            return jsonify({"error": "Expected a JSON object"}), 400
        return jsonify(build_result(payload))

    @app.post("/detect_batch")
    def detect_batch():
        payload = request.get_json(silent=True)
        if payload is None:
            return jsonify({"error": "Expected JSON body"}), 400

        items = payload
        if isinstance(payload, dict):
            items = payload.get("items")

        if not isinstance(items, list):
            return jsonify({"error": "Expected a list of items"}), 400

        results = []
        for item in items:
            if not isinstance(item, dict):
                return jsonify({"error": "Each item must be a JSON object"}), 400
            results.append(build_result(item))
        return jsonify({"results": results})

    return app


app = create_app()
