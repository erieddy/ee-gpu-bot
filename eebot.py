import time, re, logging, sys, getopt, csv, threading
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from configparser import ConfigParser


class EEbot():
    def best_buy_bot(self, bb_url, bb_user, bb_pass, desc=None):
        #self.logger.info('Best Buy URL is %s', bb_url)
        #self.logger.info('Best Buy user is %s', bb_user)
        browser = webdriver.Chrome(self.chrome_driver)

        #login
        browser.get('https://www.bestbuy.com/identity/global/signin')

        ##Input Username
        loginEmail = browser.find_elements_by_id('fld-e')
        loginEmail[0].send_keys(bb_user)

        ##Input password
        loginPassword = browser.find_elements_by_id('fld-p1')
        loginPassword[0].send_keys(bb_pass)

        #sign in
        try:
            signIn = browser.find_elements_by_class_name('btn-lg')
            signIn[0].click()
        except:
            self.logger.info('failed to find the Best Buy login button on item %s. Exiting', desc)      
        #wait for login to comnplete
        time.sleep(2)

        buyButton = False
        inStock = False

        while not buyButton:

            #Load product page    
            browser.get(bb_url)
            try: 
                addtoCartBtn = browser.find_element_by_class_name('btn-disabled')

                #print if button still disabled
                self.logger.info('The Best Buy %s is out of stock. Refreshing page to check again.', desc)

                #wait 1 second before performing hover
                time.sleep(1)

                #Perform Hover to avoid being detected
                element_to_hover_over = browser.find_element_by_class_name('logo')
                hover = ActionChains(browser).move_to_element(element_to_hover_over)
                hover.perform()

            except:
                #Attempt to add to cart set to true
                tryAddToCart = True

                #perform hover to get around bot detection 
                element_to_hover_over = browser.find_element_by_class_name('hamburger-menu')

                hover = ActionChains(browser).move_to_element(element_to_hover_over)
                hover.perform()
                print('The item is in stock! Starting Loop to add to cart')

        self.logger.info('Ending BestBuy thread')

    def amazon_bot(self, amzn_url, amzn_user, amzn_pass, desc=None):
        #self.logger.info('Amazon URL is %s', amzn_url)
        #self.logger.info('Amazon user is %s', amzn_user)
        browser = webdriver.Chrome(self.chrome_driver)

        #amazon login
        browser.get('https://www.amazon.com/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2Fref%3Dnav_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=usflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&')

        #fill in email
        emailField = browser.find_element_by_name('email')
        emailField.send_keys(amzn_user)

        #continue top next step
        contineButon = browser.find_elements_by_class_name('a-button-input')
        contineButon[0].click()

        #input password
        passwordField = browser.find_elements_by_id('ap_password')
        passwordField[0].send_keys(amzn_pass)

        try:
            #click sign in
            signInButton = browser.find_elements_by_id('signInSubmit')
            signInButton[0].click()
        except:
            self.logger.error('Failed to find the login button')
        #load item URL
        browser.get(amzn_url)
        time.sleep(2)
        self.logger.info('Ending Amazon thread')
        
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

        self.logger.info('Completed loading in the required paramters, now loading URLs')

        #Load in URLs from CSV file
        threads = list()
        with open('urls.csv', newline='') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                if row[0] == 'bestbuy':
                    x = threading.Thread(target=self.best_buy_bot, args=(row[2], self.bestbuy_user, self.bestbuy_pass, row[1],))
                elif row[0] == 'amazon':
                    x = threading.Thread(target=self.amazon_bot, args=(row[2], self.amazon_user, self.amazon_pass, row[1],))
                else:
                    self.logger.error('The site %s is invalid for row %s. Exiting code', row[0], row)
                    exit()
                threads.append(x)
                x.start()