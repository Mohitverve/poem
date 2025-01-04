from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)

# Load GPT-2 model for text generation
generator = pipeline("text-generation", model="gpt2")

@app.route('/generate', methods=['POST'])
def generate_poem():
    data = request.json
    prompt = data.get("prompt", "Write a poem about love.")
    max_length = data.get("max_length", 100)

    try:
        result = generator(prompt, max_length=max_length, num_return_sequences=1)
        poem = result[0]["generated_text"]
        return jsonify({"poem": poem})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)