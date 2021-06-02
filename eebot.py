import time
import re
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import sys, getopt
from configparser import ConfigParser


class EEbot():
    def __init__(self, logger):
        self.logger = logger
        logger.info('EE bot is intializing and loading the required paramters')

        # instantiate
        config = ConfigParser()

        # parse existing file
        config.read('config.ini')
        
        #Load driver
        self.chrome_driver = config.get('global', 'chrome_driver')

        #load creds
        self.amazon_user = config.get('amazon', 'amazon_user')
        self.amazon_pass = config.get('amazon', 'amazon_pass')

        self.bestbuy_user = config.get('bestbuy', 'bestbuy_user')
        self.bestbuy_pass = config.get('bestbuy', 'bestbuy_pass')

        self.logger.info('Completed loading in the required paramters')
   
    def load_urls():
        pass

    def best_buy_bot(self, bb_url, bb_user, bb_pass):
        pass

    def amazon_bot(self, amzn_url, amzn_user, amzn_pass):
        pass