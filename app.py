from flask import Flask, request, jsonify
import json
from chat_processor import get_response

app = Flask(__name__)

@app.route('/getResponse', methods=['POST'])
def index():
    req = request.get_json()
    req['msg'] = req['msg'].encode('utf-8').decode('utf-8')
    print(req)
    return get_response(req['idChat'], req['idUser'], req['msg'], req['name'])

if __name__ == '__main__':
    app.run(port=8001)
