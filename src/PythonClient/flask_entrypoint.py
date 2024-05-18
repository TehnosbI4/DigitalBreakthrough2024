from io import BytesIO
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from core import AudioValidator
import pydub
import base64

app = Flask(__name__)
api = Api(app)
av = AudioValidator()

@app.post('/submit_input')
def post():
    mp3_data = request.get_json()
    print(mp3_data)
    mp3_data = mp3_data['files']  # status code
    
    bins_names = []
    name = []
    for d in mp3_data:
        c_data, name = d["Content"], d["Name"]

        bins_names.append((c_data, name))

        b =  base64.b64decode(c_data)
        wav_file = open("temp.mp3", "wb")
        wav_file.write(b)

        #encode_string = base64.b64encode(open(", "rb").read())

        mp3 = pydub.AudioSegment.from_(c_data)
        print(mp3)

    preds, texts = av.full_pipeline(bin_audios_n_names=bins_names)

    decoded_data = {"data" : []}

    for i, (pred, txt) in enumerate(zip((preds, texts))):
        
        decoded_data["data"].append({
            "prediction": pred,
            "text": txt
        })

    return jsonify(decoded_data), 201

if __name__ == '__main__':
    
    #print(av.full_pipeline([f"{c_path}\\02.05.2024_00_41_02.mp3"]))
    app.run(debug=True)