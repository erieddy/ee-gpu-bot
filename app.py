import eebot
import csv
import logging
from configparser import ConfigParser


def load_creds():
    pass

def load_urls():
    pass


def load_params():
    # instantiate
    config = ConfigParser()

    # parse existing file
    config.read('config.ini')
    
    #Load driver
    chrome_driver = config.get('global', 'chrome_driver')

    #load creds
    amazon_user = config.get('amazon', 'amazon_user')
    amazon_pass = config.get('amazon', 'amazon_pass')

    bestbuy_user = config.get('bestbuy', 'bestbuy_user')
    bestbuy_pass = config.get('bestbuy', 'bestbuy_pass')

    


## start
load_params()
print('starting app')
