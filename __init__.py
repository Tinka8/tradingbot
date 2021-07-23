import os
import logging
import subprocess
import datetime
from bot import Bot
from datetime import date

# run integrity checks
result = subprocess.call("pipenv run python integrity.py", shell=True)

# exit if error is returned
if (result == 1):
    exit(1)

# current date
today = date.today()

# current day
day = datetime.datetime.now()

# current time 
now = datetime.datetime.now()

# logging mode type 
if (os.environ['LOGGING_MODE']) == 'single':
    logging_filename = 'logs/app.log'
if (os.environ['LOGGING_MODE']) == 'daily':
    logging_filename = 'logs/' + today.strftime("%Y-%m-%d") + '.log'

# setting logging library       
logging.basicConfig(filename=logging_filename, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)

# logging message
logging.info('Started')


bot = Bot()

# welcome message
print(bot.welcome())
logging.debug('Welcome text printed')

# login user
bot.login(os.environ['USER_ID'], os.environ['PASSWORD'])
print("Successfully logged in")

# set instruments
instruments = ['COCOA', 'COFFEE']

# check instruments
trading_hours = bot.get_trading_hours(instruments)

# check if market is open for specific instruments
market_open = bot.is_market_open(instruments)
if (market_open):
    print('Market for ' + ', '.join(instruments) + ' is opened now!')
else:
    print('Market for ' + ', '.join(instruments) + ' is closed now!')

# check current time and day and print market status 
if (market_open):
    print('It is ' +  (day.strftime("%A ")) +  str(now.hour) + ':' + str(now.minute) + ' and market for COCOA is opened now!')
else:
    print('It is ' +  (day.strftime("%A ")) +  str(now.hour) + ':' + str(now.minute) + ' and market for COCOA is closed now!')
