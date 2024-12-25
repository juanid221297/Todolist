from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import logging
import os
import signal

# Flask app setup
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Placeholder for the Gramformer model
gf = None

# Function to load the Gramformer model asynchronously
def load_model():
    global gf
    from gramformer import Gramformer
    try:
        logger.info("Loading Gramformer model...")
        gf = Gramformer(models=1)
        logger.info("Gramformer model loaded successfully.")
    except Exception as e:
        logger.error(f"Failed to load Gramformer model: {e}")

# Load model in a separate thread
threading.Thread(target=load_model).start()

# Signal handlers for graceful termination
def handle_exit_signal(signum, frame):
    logger.info("Received termination signal. Exiting gracefully...")
    os._exit(0)

signal.signal(signal.SIGTERM, handle_exit_signal)
signal.signal(signal.SIGINT, handle_exit_signal)

@app.route('/', methods=['POST'])
def check_grammar():
    if not gf:
        return jsonify({"error": "Model is still loading. Please try again later."}), 503

    try:
        data = request.json
        if not data or "sentence" not in data:
            return jsonify({"error": "No sentence provided"}), 400
        
        sentence = data["sentence"]
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
