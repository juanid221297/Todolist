from flask import Flask, request, jsonify
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
import torch
from PIL import Image
import io
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Global variables for lazy loading
model, feature_extractor, tokenizer, device = None, None, None, None

def load_model():
    """Lazy load the model, tokenizer, and feature extractor."""
    global model, feature_extractor, tokenizer, device
    if model is None:
        print("Loading model, tokenizer, and feature extractor...")
        # Load the model components
        model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
        feature_extractor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
        tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

        # Set the device (GPU if available)
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model.to(device)

        # Use half precision on GPU for memory optimization
        if device.type == "cuda":
            model.half()
        print("Model loaded successfully.")

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

        # Convert the image into pixel values
        pixel_values = feature_extractor(images=[image], return_tensors="pt", padding=True).pixel_values
        pixel_values = pixel_values.to(device)

        # Generate text from the pixel values
        output_ids = model.generate(pixel_values, **gen_kwargs)
        preds = tokenizer.batch_decode(output_ids, skip_special_tokens=True)
        return preds[0].strip()
    except Exception as e:
        return f"Error processing the image: {e}"

@app.route('/')
def home():
    """Default route for the API."""
    return "Welcome to the Image-to-Text Captioning API!", 200

@app.route('/predict', methods=['POST'])
def predict():
    """Endpoint to handle prediction requests."""
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        # Read the image file
        image = file.read()

        # Load the model lazily
        load_model()

        # Generate a caption for the image
        caption = predict_step(image, model, feature_extractor, tokenizer, device)
        return jsonify({"caption": caption}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Use the PORT environment variable set by Render, default to 5000 for local testing
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
