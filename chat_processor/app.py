from flask import Flask, request, jsonify
import json
from chat_processor import get_response, init as initCP
from spell_checker import init as initSC
from config import NOTIFICATION_TASK_INTERVAL
from periodic_message import msg_inactive_users
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

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

    get_response(req['idChat'], req['idUser'], req['msg'], req['name'], req['timestamp'], location)
    return "success"

if __name__ == '__main__':
    #Job for periodic message
    scheduler = BackgroundScheduler()
    scheduler.add_job(msg_inactive_users, 'interval', minutes=NOTIFICATION_TASK_INTERVAL)
    scheduler.start()

    app.run(host='0.0.0.0', port=5001, threaded=True)
