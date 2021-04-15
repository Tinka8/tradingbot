import os 
import logging

# log error, print error for user and die
def log_die(message):
    # log
    logging.basicConfig(filename='logs/integrity.log', format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)
    logging.critical(message)
    
    # print
    print(message)

    # die
    exit(1)

# 1001 check if logging mode is set
if "LOGGING_MODE" not in os.environ:
    log_die('[1001] Logging mode environment variable is not set')