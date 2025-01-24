import os
from flask import Flask, request, jsonify
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
import torch
from PIL import Image
import io
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Lazy load model components
model, feature_extractor, tokenizer, device = None, None, None, None

def load_model():
    """Preload the model, tokenizer, and feature extractor."""
    global model, feature_extractor, tokenizer, device
    if model is None:
        print("Loading model...")
        model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
        feature_extractor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
        tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model.to(device)
        if device.type == "cuda":
            model.half()
        print("Model loaded successfully.")

@app.before_first_request
def preload_model():
    """Preload the model before handling the first request."""
    load_model()

def predict_step(image, model, feature_extractor, tokenizer, device):
    """Generate a caption for an image."""
    max_length = 16
    num_beams = 4
    gen_kwargs = {"max_length": max_length, "num_beams": num_beams}

    try:
        # Open and process the image
        image = Image.open(io.BytesIO(image))
        if image.mode != "RGB":
            image = image.convert(mode="RGB")
        pixel_values = feature_extractor(images=[image], return_tensors="pt", padding=True).pixel_values
        pixel_values = pixel_values.to(device)

        # Generate text from the image
        output_ids = model.generate(pixel_values, **gen_kwargs)
        preds = tokenizer.batch_decode(output_ids, skip_special_tokens=True)
        return preds[0].strip()
    except Exception as e:
        return f"Error processing the image: {e}"

@app.route('/')
def home():
    return "Welcome to the Image-to-Text Captioning API!"

@app.route('/predict', methods=['POST'])
def predict():
    """Endpoint to handle prediction requests."""
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        image = file.read()
        caption = predict_step(image, model, feature_extractor, tokenizer, device)
        return jsonify({"caption": caption}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Increase Gunicorn timeout
    os.environ["GUNICORN_CMD_ARGS"] = "--timeout 120"
    
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
