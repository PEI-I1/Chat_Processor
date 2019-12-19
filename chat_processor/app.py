from flask import Flask, request, jsonify
import json
from chat_processor import get_response, init as initCP
from spell_checker import init as initSC

app = Flask(__name__)
#init necessary components Chat Processor and Spell Checker
initCP()
initSC()

@app.route('/getResponse', methods=['POST'])
def index():
    req = request.get_json()
    req['msg'] = req['msg'].encode('utf-8').decode('utf-8')
    print(req)
    if req['location'] and 'lat' in req['location'] and 'lon' in req['location']:
        location = {'lat': req['location']['lat'], 'lon': req['location']['lon']}
    else:
        location = None

    get_response(req['idChat'], req['idUser'], req['msg'], req['name'], location)
    return "success"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, threaded=True)
