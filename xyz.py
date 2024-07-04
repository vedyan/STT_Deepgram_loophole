from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from deepgram import Deepgram
from deepgram import DeepgramClient, PrerecordedOptions
import base64
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
port = int(os.environ.get("PORT", 5000))
CORS(app)  # Enable CORS for all routes
API_KEY = os.getenv("DG_API_KEY")
deepgram = DeepgramClient(API_KEY)
@app.route('/')
def index():
    return render_template('xyz.html')
@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    try:
        # Receive base64 encoded audio chunk from frontend
        data = request.json.get('audio_chunk')

        # Decode base64 and save as .wav file
        audio_bytes = base64.b64decode(data)
        file_path = 'temp.wav'
        with open(file_path, 'wb') as file:
            file.write(audio_bytes)

        # Transcribe the audio chunk using Deepgram
        with open(file_path, 'rb') as file:
            buffer_data = file.read()

        payload = {
            "buffer": buffer_data,
        }

        options = PrerecordedOptions(
            model="nova-2",
            smart_format=True,
        )

        response = deepgram.listen.prerecorded.v("1").transcribe_file(payload, options)

        transcribed_text = response['results']['channels'][0]['alternatives'][0]['transcript']

        # Return the transcribed text to the frontend
        print(transcribed_text)
        return jsonify({'transcript': transcribed_text}), 200

    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)