from eebot import EEbot
import csv
import logging



## start
logger = logging.getLogger()
logging.basicConfig(
    format='[%(asctime)s] %(levelname)-8s  %(name)-12s  %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')
logger.info('Starting the EEbot app loader script')

EEbot(logger)