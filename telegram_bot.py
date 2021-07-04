import requests #
import json
import configparser as cfg # 
class telegram_chatbot():

    def __init__(self, config):
        self.token = self.read_token_from_config_file(config)
        self.base = "https://api.telegram.org/bot{}/".format(self.token)

    def get_updates(self, offset=None):
        url = self.base + "getUpdates?timeout=1"
        if offset:
            url = url + "&offset={}".format(offset+1)
        r = requests.get(url)
        return json.loads(r.content)

    def send_message(self, msg, chat_id):
        url = self.base + "sendMessage?chat_id={}&text={}".format(chat_id, msg)
        if msg is not None:
            requests.get(url)

    def send_document(self,from_,file):
        files = {'document':open(file,'rb')}
        if files:
            requests.get(self.base + "senddocument?chat_id={}".format(from_),files=files)

    def read_token_from_config_file(self, config):
        parser = cfg.ConfigParser()
        parser.read(config)
        return parser.get('creds', 'token')

telegram_chatbot.get_updates