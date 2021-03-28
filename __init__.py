import os
import logging
from bot import Bot
from datetime import date

# current date
today = date.today()

# logging mode type 
if (os.environ['LOGGING_MODE']) == 'single':
    logging_filename = 'logs/app.log'
if (os.environ['LOGGING_MODE']) == 'daily':
    logging_filename = 'logs/' + today.strftime("%Y-%m-%d") + '.log'

# setting logging library       
logging.basicConfig(filename=logging_filename, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)

# logging message
logging.info('Started')


message = Bot()
# welcome message
print(message.welcome())
logging.debug('Welcome text printed')

