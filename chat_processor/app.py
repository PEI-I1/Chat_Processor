from flask import Flask, request, jsonify
import json
from chat_processor import get_response, init as initCP
from spell_checker import init as initSC

app = Flask(__name__)
initCP()
initSC()

@app.route('/getResponse', methods=['POST'])
def index():
    req = request.get_json()
    req['msg'] = req['msg'].encode('utf-8').decode('utf-8')
    print(req)
    return get_response(req['idChat'], req['idUser'], req['msg'], req['name'])

if __name__ == '__main__':
    app.run(port=5001)
