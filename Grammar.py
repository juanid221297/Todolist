from flask import Flask, request, jsonify
from gramformer import Gramformer
from flask_cors import CORS
from multiprocessing import active_children
import atexit
import os
import signal

app = Flask(__name__)  # Create the Flask app object
CORS(app, resources={r"/*": {"origins": "*"}})  # Enable CORS for all routes

# Load the Gramformer model globally during startup
gf = Gramformer(models=1)  # Grammar correction model

# Function to clean up all active child processes
def cleanup_processes():
    for process in active_children():
        process.terminate()
        process.join()

# Register the cleanup function to be called during application exit
atexit.register(cleanup_processes)

# Ensure termination signals are handled
def handle_exit_signal(signum, frame):
    cleanup_processes()
    os._exit(0)  # Exit the application

# Set signal handlers
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
        app.logger.error(f"Error occurred: {e}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use PORT env variable if available, else default to 5000
    app.run(host="0.0.0.0", port=port, debug=True)
