from io import BytesIO
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from core import AudioValidator
import pydub
import base64
from flask import json

json.provider.DefaultJSONProvider.ensure_ascii = False

app = Flask(__name__)
api = Api(app)
av = AudioValidator()

@app.post('/submit_input')
def post():
    mp3_data = request.get_json()
    print(mp3_data)
    mp3_data = mp3_data['files']  # status code
    
    paths = []
    for d in mp3_data:
        path =d["Content"]

        paths.append(path)

    preds, texts = av.full_pipeline(paths=paths)

    decoded_data = {"data" : []}

    for pred, txt in zip(preds, texts):
        print(pred, txt)
        decoded_data["data"].append({
            "prediction": str(pred),
            "text": txt
        })

    return jsonify(decoded_data), 201

if __name__ == '__main__':
    
    #print(av.full_pipeline([f"{c_path}\\02.05.2024_00_41_02.mp3"]))
    app.run(debug=True)