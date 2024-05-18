from flask import Flask, jsonify, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

@app.post('/submit_input')
def post():
    data = request.get_json()  # status code
    print("224")
    return jsonify({'data': data}), 201

if __name__ == '__main__':
    
    app.run(debug=True)