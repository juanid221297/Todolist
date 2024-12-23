from flask import Flask, request, jsonify
import language_tool_python

app = Flask(__name__)
tool = language_tool_python.LanguageTool('en-US')

@app.route('/check_grammar', methods=['POST'])
def check_grammar():
    data = request.json
    sentence = data.get("sentence", "")
    if not sentence:
        return jsonify({"error": "No sentence provided"}), 400
    
    matches = tool.check(sentence)
    if not matches:
        return jsonify({"message": "Your sentence is correct!"})
    
    errors = []
    for match in matches:
        errors.append({
            "issue": match.message,
            "suggestion": match.replacements,
            "context": match.context
        })
    
    return jsonify({"errors": errors})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
