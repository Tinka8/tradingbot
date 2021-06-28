import os
import enum 
import json
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
    
    def _send_command(self, dict_data):
        """send command to api"""

        logging.info('Sending command: ' + dict_data["command"])
        
        self.ws.send(json.dumps(dict_data))
        response = self.ws.recv()
        
        result = json.loads(response)
        if result['status'] is True:
            logging.info('Executed command: ' + dict_data["command"])

        return result
 