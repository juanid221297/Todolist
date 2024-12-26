from flask import Flask, request, jsonify
import language_tool_python

app = Flask(__name__)

# Initialize the LanguageTool client
tool = language_tool_python.LanguageTool('en-US')

@app.route('/check_grammar', methods=['POST'])
def check_grammar():
    # Check if the text was provided in the request
    if 'text' not in request.json:
        return jsonify({'error': 'No text provided'}), 400
    
    text = request.json['text']
    
    # Check the grammar of the provided text
    matches = tool.check(text)
    
    if len(matches) == 0:
        return jsonify({'message': 'Your sentence is grammatically correct!'})
    
    # Correct the text based on the detected mistakes
    corrected_text = language_tool_python.utils.correct(text, matches)
    
    # Prepare the response with errors and corrections
    errors = [{'message': match.message, 'error': match.context, 'replacement': match.replacements} for match in matches]
    
    return jsonify({
        'message': 'Your sentence contains grammar issues.',
        'errors': errors,
        'corrected_text': corrected_text
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
