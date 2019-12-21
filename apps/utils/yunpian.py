import requests
import json


class YunPian:
    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = ''

    def send_sms(self, code, mobile):
        parmas = {
            "apikey": self.api_key,
            "mobile": mobile,
            "text": code
        }

        response = requests.post(self.single_send_url, data=parmas)
        re_dict = json.loads(response.text)
        return re_dict

