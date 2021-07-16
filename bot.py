import os
import enum 
import json
import logging
import datetime
from websocket import create_connection
from datetime import date

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
        
    def is_market_open(self, instruments): 
        open_time = datetime.time(hour = 10, minute = 45, second = 0)
        close_time = datetime.time(hour = 19, minute = 30, second = 0)
        today = date.today()
        # check if time is between 10.45 and 19.30
        if today.time() <= open_time or today.time() >= close_time:
            return True
        else:
            print("Market for COCOA is closed now!")
        # check if it's weekday today 
        if today.date().weekday() <= 5:
            return True  
        else:
            print("Market for COCOA is closed now!")
