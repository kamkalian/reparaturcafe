from app.oskar_bot import bp
from app.models import Onlinecheck, Log
from flask import request, Response
from app.config import Config
import re
import requests


def parse_message(message):

    # Information aus dem übergebenen JSON (message) extrahieren
    chat_id = message['message']['chat']['id']
    txt = message['message']['text']
    first_name = message['message']['from']['first_name']

    # regex Pattern zum Filtern der Befehle
    pattern = r'/[a-zA-Z]{2,5}'

    # regex Filter anwenden
    cmd_list = re.findall(pattern, txt)

    if cmd_list: 
        cmd = cmd_list[0][1:].upper() # /start > start   .strip('/')
    else:
        cmd = ''

    return chat_id, cmd, first_name


def send_message(chat_id, text, parse_mode=''):
    # Url aus der Telegram API, in der url steckt der Token des Bots
    url = f'https://api.telegram.org/bot{Config.TELEGRAM_BOT_TOKEN}/sendMessage'

    # Über den Payload wird als Json die Chat id und der Text mitgeschickt.
    payload = {'chat_id':chat_id, 'text':text, 'parse_mode':parse_mode}

    # Ein POST request wird gesendet.
    r = requests.post(url, json=payload)
    return r


@bp.route('/oskar_bot', methods=['POST', 'GET'])
def oskar_bot():

    # Über diese Route schickt Telegram Post Requests sobald jemand etwas schreibt.
    # Dazu muss über die Telegram API ein Webhook eingerichtet werden.
    # z.B. https://api.telegram.org/bot<token>/setWebhook?url=https://q01.reparaturcafe.online/oskar_bot
    
    # Wenn ein Post request rein kommt dann hat jemand etwas im Telegram Chat geschrieben.
    if request.method == 'POST':

        # Im mitgelieferten Json steckt die Message
        msg = request.get_json()

        # Die Message wird auf enthaltene Befehle untersucht
        chat_id, cmd, first_name = parse_message(msg)

        # Prüfen welcher Befehl gesendet wurde und entsprechend reagieren
        if chat_id == '422828332':
            # HALLO der Bot stellt sich kurz vor
            if cmd == 'HALLO':
                send_message(chat_id, 'Hallo, ich bin Oskar, der Bot des Reparaturcafes in der AWO Oberlar.<br>Folgende Befehle kann ich schon: /hallo /list')
            
            # LIST listet alle offenen Onlinechecks auf
            if cmd == 'LIST':
                oc_list = Onlinecheck.query.filter(
                        ~Onlinecheck.logs.any(Log.state=='closed')
                ).all()
                device_list = []
                for oc in oc_list:
                    device_list.append(oc.device_name)
                send_message(chat_id, device_list)
        else:
            send_message(chat_id, f'Hallo {first_name}, bitte nutze den direkten Chat zum Bot: @oskar_awo_bot, um Befehle auszuführen.\nSomit werden dann die anderen Teilnehmer in dieser Gruppe nicht gestört.')

        return Response('Ok', status=200)
    else:
        return '<h1>Oskar AWO Bot for Telegram</h1>'



# https://api.telegram.org/bot<token>/getMe