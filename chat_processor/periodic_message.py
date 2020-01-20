from config import INACTIVE_TIME
from prefab_msgs import prefab_msgs
from pretty_print import reset
from utils import send_silent_msg
from datetime import datetime, timedelta

chats_timestamps = {}

def save_chat_timestamp(idChat, idUser, timestamp):
    chats_timestamps[idChat] = (idUser, timestamp)

def msg_inactive_users():
    now = datetime.now()
    for idChat in list(chats_timestamps):
        entry = chats_timestamps[idChat]
        idUser = entry[0]
        timestamp = entry[1]

        dt = datetime.fromtimestamp(timestamp)
        # check if last message was more than 'INACTIVE_TIME' time ago
        if dt < now - timedelta(minutes=INACTIVE_TIME):
            # reset chat state
            reset(idChat, idUser, True)
            # send message
            send_silent_msg(idChat, prefab_msgs["about"][2])
            # remove from dictionary to make sure user don't receive the message more than one time
            del chats_timestamps[idChat]
