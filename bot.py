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
        if result['status'] is False:
            raise CommandFailed(result)
        else:
            logging.info('Executed command: ' + dict_data["command"])

        if 'returnData' in result.keys():
            logging.info("CMD: done")
            logging.debug(result['returnData'])
            return result['returnData']

        return result
    
    def get_trading_hours(self, instruments):
        
        data = {
            "command": "getTradingHours",
            "arguments" : {
                "symbols": instruments
            }
        }

        return self._send_command(data)
        
    # check if market is currently opened for all listed instruments
    # @use is_market_open(['COCOA', 'COFFEE'])
    def is_market_open(self, instruments):
        # get opening hours for listed instruments
        opening_hours = self.get_trading_hours(instruments)

        # store opened/closed per instrument
        results = []

        # loop over each instrument
        for index, instrument in enumerate(instruments):
            # store opening hours for specific instrument in local variable
            instrument_opening_hours = opening_hours[index]

            # get which weekday is today
            weekday = date.today().weekday()

            # define opening times for today
            times = []

            # loop over all opening hours
            for opening in instrument_opening_hours['trading']:
                # consider opening hours for current weekday
                if (opening['day'] == weekday):
                    times.append({
                        'fromT': opening['fromT'],  # in milliseconds from midnight
                        'toT'  : opening['toT']     # in milliseconds from midnight
                    })

            # define current milliseconds from midnight
            now = datetime.datetime.now()
            milliseconds_since_midnight = (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds() * 1000

            # set default value for opened/closed
            opened = False

            for opening_time in times:
                if (opening_time['fromT'] < milliseconds_since_midnight and opening_time['toT'] > milliseconds_since_midnight):
                    opened = True
            
            # store result in list of results
            results.append({
                'instrument': instrument,
                'opened'    : opened
            })
        
        # get only closed
        closed = list(filter(self.check_is_closed_result, results))
        
        # return true, if all checked instruments are opened (array of closed is empty)
        return len(closed) == 0

    def check_is_closed_result(self, result):
        return result['opened'] != True

    def check_is_opened_result(self, result):
        return result['opened']

    def welcome(self):

        return self.welcome_text