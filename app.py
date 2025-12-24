import argparse

from flask import Flask, jsonify, request

from lang_detect import analyze_text

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


def build_result(payload):
    text = payload.get("text", "")
    result = analyze_text(text)
    result["id"] = payload.get("id", "")
    return result


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


def main(argv=None):
    parser = argparse.ArgumentParser(description="Flask server for language detection.")
    parser.add_argument("--host", default="127.0.0.1", help="Host interface to bind")
    parser.add_argument("--port", type=int, default=5000, help="Port to bind")
    parser.add_argument("--debug", action="store_true", help="Enable Flask debug mode")
    args = parser.parse_args(argv)
    app.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == "__main__":
    main()
