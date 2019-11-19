from app.oskar_bot import bp
from app.models import Onlinecheck, Log
from flask import request, Response
from app.config import Config
import re
import requests
import pickle


def parse_message(message):

    # Information aus dem übergebenen JSON (message) extrahieren
    chat_id = message['message']['chat']['id']
    txt = message['message']['text']
    first_name = message['message']['from']['first_name']

    # regex Pattern zum Filtern der Befehle; Unterstrich wird auch erlaubt.
    pattern = r'/[a-zA-Z_]{2,7}'

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

    '''
    Über diese Route schickt Telegram Post Requests sobald jemand etwas schreibt.
    Dazu muss über die Telegram API ein Webhook eingerichtet werden.
    z.B. https://api.telegram.org/bot<token>/setWebhook?url=https://q01.reparaturcafe.online/oskar_bot
    '''
    
    # Aus einer Datei wird die aktuel cmd_off_list geholt
    try:
        with open('cmd_off_list.p', 'rb') as f:
            cmd_off_list = pickle.load(f)
    except FileNotFoundError:
        cmd_off_list = []
        with open('cmd_off_list.p', 'wb') as f:
            pickle.dump(cmd_off_list, f)
    
    # Wenn ein Post request rein kommt dann hat jemand etwas im Telegram Chat geschrieben.
    if request.method == 'POST':

        # Im mitgelieferten Json steckt die Message
        msg = request.get_json()

        # Die Message wird auf enthaltene Befehle untersucht
        chat_id, cmd, first_name = parse_message(msg)

        # CMD_ON; hiermit wird die chat_id wieder von der Liste runter genommen.
        if cmd == 'CMD_ON':

            # chat_id entfernen
            try:
                cmd_off_list = cmd_off_list.remove(chat_id)
            except ValueError:
                send_message(chat_id, 'In diesem Chat anworte ich schon auf jedes Kommando.')
                return Response('Ok', status=200)

            # Wenn nach dem Entfernen die List = None ist so wird eine leere Liste erstellt
            if not cmd_off_list:
                cmd_off_list = []

            # Liste in Datei speichern
            with open('cmd_off_list.p', 'wb') as f:
                pickle.dump(cmd_off_list, f)

            # Antwort senden
            send_message(chat_id, 'Juhu, jetzt darf ich wieder auf Kommandos antworten.')
            return Response('Ok', status=200)

        # Prüfen ob es erlaubt ist in diesem Chat auf einen Befehl zu Antworten
        if chat_id not in cmd_off_list:

            # CMD_OFF; wenn der Bot den befehl 'cmd_off' bekommt dann wird die chat_id auf eine Liste gesetzt
            if cmd == 'CMD_OFF':
                cmd_off_list.append(chat_id)
                with open('cmd_off_list.p', 'wb') as f:
                    pickle.dump(cmd_off_list, f)
                send_message(chat_id, 'Ok, ich werde ab sofort in diesem Chat nicht mehr auf Kommandos antworten.\nWenn Ihr das wieder ändern wollt gebt einfach /cmd_on ein.')
                return Response('Ok', status=200)

            # HALLO; der Bot stellt sich kurz vor
            if cmd == 'HALLO':
                send_message(chat_id, 'Hallo, ich bin Oskar, der Bot des Reparaturcafes in der AWO Oberlar.\nFolgende Befehle kann ich schon: \n/hallo\n/list\n/cmd_off\n/cmd_on')
            
            # LIST; listet alle offenen Onlinechecks auf
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