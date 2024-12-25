from flask import Flask, request, jsonify
from gramformer import Gramformer
from flask_cors import CORS

app = Flask(__name__)  # Create the Flask app object
CORS(app)  # Initialize CORS after the app is created

gf = Gramformer(models=1)  # 1 for grammar correction model

@app.route('/check_grammar', methods=['POST'])
def check_grammar():
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
