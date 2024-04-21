from flask import Flask, request, jsonify
from flask_cors import CORS
import fitz  # PyMuPDF
from werkzeug.utils import secure_filename
from openai import OpenAI
import os
from os.path import join, dirname
from dotenv import load_dotenv
import tiktoken

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

app = Flask(__name__)
CORS(app)  # CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

# Set up a directory to save uploaded files
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613"):
  """Returns the number of tokens used by a list of messages."""
  try:
      encoding = tiktoken.encoding_for_model(model)
  except KeyError:
      encoding = tiktoken.get_encoding("cl100k_base")
  if model == "gpt-3.5-turbo-0613":  # note: future models may deviate from this
      num_tokens = 0
      for message in messages:
          num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
          for key, value in message.items():
              num_tokens += len(encoding.encode(value))
              if key == "name":  # if there's a name, the role is omitted
                  num_tokens += -1  # role is always required and always 1 token
      num_tokens += 2  # every reply is primed with <im_start>assistant
      return num_tokens
  else:
      raise NotImplementedError(f"""num_tokens_from_messages() is not presently implemented for model {model}.
  See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.""")

@app.route('/fix-text', methods=['POST'])
def fix_text():
    input_text = request.json["text"]

    responses = []
    for segment in input_text:
        messages = [
            {
                "role": "user",
                "content": f"{segment}"
            },
            {
                "role": "user",
                "content": "Reconstitue l'entièreté du texte ci-dessus. Ne résume pas le texte, n'enlève pas d'informations, ne change pas le sens du texte."
            },
        ]
        token_count = num_tokens_from_messages(messages)
        if token_count > 4096:
            # go to the next segment
            continue
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-16k-0613",
            messages=messages,
            max_tokens=16384 - token_count,
            temperature=0.0,
            top_p=0.5,
            frequency_penalty=0.0,
            presence_penalty=0.0,
        )
        print(response.choices[0].message.content)
        responses.append(response.choices[0].message.content)

    return jsonify({"responses": responses})

@app.route('/upload-pdf', methods=['POST'])
def upload_pdf():
    # Check if the request has the file part
    if 'pdfFile' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['pdfFile']
    # If user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and file.filename.endswith('.pdf'):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        text = extract_text_from_pdf(filepath)
        # Delete the uploaded file
        os.remove(filepath)
        return jsonify({"pages": text})
    else:
        return jsonify({"error": "Unsupported file type"}), 400

def extract_text_from_pdf(filepath):
    pdf_document = fitz.open(filepath)
    output = []
    for page in pdf_document:
        output.append(page.get_text())
    return output

if __name__ == '__main__':
    app.run(debug=True)
