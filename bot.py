import os
import enum 
import json
import logging
from websocket import create_connection

class STATUS(enum.Enum):
    LOGGED = enum.auto()
    NOT_LOGGED = enum.auto()
    
class Bot:
    def __init__(self):
        
        self.welcome_text = '====================\nXTB Trading bot\n@author Tinka8\n@version 0.0.2\n===================='
        self.ws = None
        self.status = STATUS.NOT_LOGGED
    
    def welcome(self):

        return self.welcome_text
        
    def login(self, user_id, password, mode='demo'):
        """login command"""

        data = {
            "command": "login",
            "arguments" : {
                "userId": user_id,
                "password": password
            }
        }

        self.ws = create_connection(f"wss://ws.xtb.com/{mode}")
        response = self._send_command(data)
        self.status = STATUS.LOGGED

        return response

    def _send_command(self, dict_data):
        """send command to api"""

        logging.info('Sending command: ' + dict_data["command"])
        
        self.ws.send(json.dumps(dict_data))
        response = self.ws.recv()
        
        result = json.loads(response)
        if result['status'] is True:
            logging.info('Executed command: ' + dict_data["command"])

        return result
    
    def get_trading_hours(self, instruments):
        
        data = {
            "command": "getTradingHours",
            "arguments" : {
                "symbols": instruments
            }
        }

        return self._send_command(data)
        

