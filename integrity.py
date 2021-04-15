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
