from flask import Flask, request, jsonify
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
from huggingface_hub import hf_hub_download
import torch
from PIL import Image
import io
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

model, feature_extractor, tokenizer, device = None, None, None, None

def load_model():
    """Lazy load the model, tokenizer, and feature extractor."""
    global model, feature_extractor, tokenizer, device
    if model is None:
        print("Loading model, tokenizer, and feature extractor...")

        # Use `hf_hub_download` with `force_download=True` for robustness
        model_path = hf_hub_download(repo_id="nlpconnect/vit-gpt2-image-captioning", 
                                     filename="pytorch_model.bin", 
                                     force_download=True)
        tokenizer_path = hf_hub_download(repo_id="nlpconnect/vit-gpt2-image-captioning", 
                                         filename="tokenizer_config.json", 
                                         force_download=True)
        feature_extractor_path = hf_hub_download(repo_id="nlpconnect/vit-gpt2-image-captioning", 
                                                 filename="preprocessor_config.json", 
                                                 force_download=True)

        model = VisionEncoderDecoderModel.from_pretrained(model_path)
        feature_extractor = ViTImageProcessor.from_pretrained(feature_extractor_path)
        tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)

        # Use half precision if supported and set device
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model.to(device)
        if device.type == "cuda":
            model.half()  # Use half precision on GPU for memory optimization
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

        pixel_values = feature_extractor(images=[image], return_tensors="pt", padding=True).pixel_values
        pixel_values = pixel_values.to(device)

        # Generate text
        output_ids = model.generate(pixel_values, **gen_kwargs)
        preds = tokenizer.batch_decode(output_ids, skip_special_tokens=True)
        return preds[0].strip()
    except Exception as e:
        return f"Error processing the image: {e}"

@app.route('/predict', methods=['POST'])
def predict():
    """Endpoint to handle prediction requests."""
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        # Get the image from the request
        image = file.read()

        # Load the model lazily (only if needed)
        load_model()

        # Generate text from the image
        caption = predict_step(image, model, feature_extractor, tokenizer, device)
        return jsonify({"caption": caption}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
