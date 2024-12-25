from flask import Flask, request, jsonify
from gramformer import Gramformer
from flask_cors import CORS
import os
import signal
import logging

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load Gramformer model during startup
gf = None
try:
    logger.info("Loading Gramformer model...")
    gf = Gramformer(models=1)
    logger.info("Gramformer model loaded successfully.")
except Exception as e:
    logger.error(f"Failed to load Gramformer model: {e}")
    raise

# Signal handlers for graceful termination
def handle_exit_signal(signum, frame):
    logger.info("Received termination signal. Exiting gracefully...")
    os._exit(0)

signal.signal(signal.SIGTERM, handle_exit_signal)
signal.signal(signal.SIGINT, handle_exit_signal)

@app.route('/', methods=['POST'])
def check_grammar():
    try:
        data = request.json
        sentence = data.get("sentence", "")
        if not sentence:
            return jsonify({"error": "No sentence provided"}), 400

        corrected_sentences = gf.correct(sentence, max_candidates=1)
        corrected_sentence = corrected_sentences[0] if corrected_sentences else sentence

        if corrected_sentence == sentence:
            return jsonify({"message": "Your sentence is correct!"})

        return jsonify({
            "original": sentence,
            "corrected": corrected_sentence
        })
    except Exception as e:
        logger.error(f"Error occurred during grammar check: {e}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    logger.info(f"Starting server on port {port}...")
    app.run(host="0.0.0.0", port=port, debug=False)
