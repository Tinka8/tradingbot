import os
import logging
from bot import Bot
from datetime import date

# welcome message
message = Bot()
print(message.welcome())

# current date
today = date.today()

# logging mode type 
if (os.environ['LOGGING_MODE']) == 'single':
    logging_filename = 'logs/app.log'
if (os.environ['LOGGING_MODE']) == 'daily':
    logging_filename = 'logs/' + today.strftime("%Y-%m-%d") + '.log'

# setting logging library       
logging.basicConfig(filename=logging_filename, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)

# logging messages
logging.info('Started')
logging.debug('Welcome text printed')


