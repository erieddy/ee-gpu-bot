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
            self.logger.info('[bestbuy] failed to find the Best Buy login button on item "%s", Exiting', desc)      
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
                self.logger.info('[bestbuy] The "%s" is out of stock. Refreshing page to check again.', desc)

                #wait 1 second before performing hover
                time.sleep(1)

                #Perform Hover to avoid being detected
                element_to_hover_over = browser.find_element_by_class_name('logo')
                hover = ActionChains(browser).move_to_element(element_to_hover_over)
                hover.perform()

            except:
                self.logger.info('[bestbuy] The "%s" is in stock! Attempting to add to cart', desc)
            

                #perform hover to get around bot detection 
                element_to_hover_over = browser.find_element_by_class_name('logo')

                hover = ActionChains(browser).move_to_element(element_to_hover_over)
                hover.perform()
                
                try:                       
                    #try to add to cart
                    addtoCartBtn  = browser.find_element_by_class_name('btn-primary')
                    addtoCartBtn.click()

                    #wait for page to load secondary step to checkout
                    time.sleep(4)

                    #Find move to cart button
                    movetoCartBtn = browser.find_elements_by_class_name('btn-secondary')
                    #Click move to cart the last item in the list 
                    self.logger.info('[bestbuy] Moving to cart button with lenght of %d', len(movetoCartBtn))
                    
                    movetoCartBtn[-1].click()

                    self.logger.info('[bestbuy] Successfuly added "%s" to the cart. Ending refresh loop.', desc)
                    buyButton = True

                    #wait for cart page to load
                    time.sleep(2)

                    #Find checkout button
                    checkoutBtn = browser.find_elements_by_class_name('btn-primary')

                    #click checkout button
                    self.logger.info('[bestbuy] Checkout button length %d',  len(checkoutBtn))
                    checkoutBtn[0].click()
                    time.sleep(10)

                    #select 12 months finacing 
                    finance12 = browser.find_element_by_id('reward-calculator-7')
                    finance12.click()
                    time.sleep(2)

                    #Purchase Item
                    purchase = browser.find_element_by_class_name('button__fast-track')
                    purchase.click()

                except:
                    #add to cart failed 
                    self.logger.error('[bestbuy] Failed to add "%s" to cart. Reloading page.', desc)

        self.logger.info('[bestbuy] Ending thread')

    def amazon_bot(self, amzn_url, amzn_user, amzn_pass, amzn_max_price, desc=None):
        #self.logger.info('Amazon URL is %s', amzn_url)
        #self.logger.info('Amazon user is %s', amzn_user)
        browser = webdriver.Chrome(self.chrome_driver)

        '''amazon login'''
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
            self.logger.error('[amazon] Failed sign in to Amazon. Unable to find the login button.')

        time.sleep(2)
        self.logger.info('Pulling ASIN from URL.')
        asinCodeTemp = re.findall("B0[A-Z,0-9]\w+", amzn_url)
        asinCode = asinCodeTemp[0]
        asinCode = asinCode.strip()
        self.logger.info('ASIN code is "' + asinCode +'".')
        url = 'https://www.amazon.com/gp/aws/cart/add.html?AssociateTag=brobot02-20&AWSAccessKeyId=AKIAIVQ27DOD3FLEYHJA&Quantity.1=1&ASIN.1=' + asinCode
        self.logger.info('[amazon] Clicking Amazon link for the "%s" with URL "%s"',  desc, url)

        amzn_check_stock = True
        while amzn_check_stock:
            time.sleep(2)
            #Getting page
            browser.get(url)

            '''Check price to make sure it is not more than the max'''
            try: 
                itemPrice = browser.find_element_by_class_name('price.item-row').text
            except: 
                self.logger.error('[amazon] Unable to find the "%s" price, it must be out of stock. Reload page and checking again.', desc)
                continue

            '''Striping out extra characters in price'''
            itemPrice = itemPrice.replace('$','')
            itemPrice = itemPrice.replace(',','')
            itemPrice = itemPrice.split('.')
            #<td nowrap="" class="price.item-row" valign="top">$1,699.99</td>
            self.logger.info('[amazon] The price of the "%s" is %s.', desc, itemPrice[0])
            if itemPrice[0] < amzn_max_price:
                self.logger.info('[amazon] The price of %s is lower than the max price of %s for item "%s"', itemPrice[0], amzn_max_price, desc)
                '''Price is good attempting to add to cart}'''
                try:
                    browser.find_element_by_name('add').click()
                except:
                    self.logger.error('Failed to click add to cart button')

                self.logger.info('[amazon] Attempting to move item to checkout for %s', desc)
                try:
                    browser.find_element_by_name('proceedToRetailCheckout').click()
                    time.sleep(2)
                except:
                    self.logger.error("[amazon] Can't find move to cart button")

                #place order
                try:
                    self.logger.info('Clicking the checkout button on %s', desc)
                    browser.find_element_by_name('placeYourOrder1').click()

                except:
                    self.logger.error('[amazon] Failed to click place order')
                '''Price is good so breaking out of while loop'''
                amzn_check_stock = False
            else: 
                self.logger.info('[amazon] The price of %s is higher than the max price of %s for item "%s". Refreshing page and checking again.', itemPrice[0], amzn_max_price, desc)
            #time.sleep(2)

        self.logger.info('[amazon] Ending thread')

    def newegg_bot(self, newegg_url, newegg_user, newegg_pass, desc=None):
        pass    
    
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
        self.amazon_max_price = config.get('amazon', 'amazon_max_price')

        self.bestbuy_user = config.get('bestbuy', 'bestbuy_user')
        self.bestbuy_pass = config.get('bestbuy', 'bestbuy_pass')

        self.newegg_user = config.get('newegg', 'newegg_user')
        self.newegg_pass = config.get('newegg', 'newegg_pass')    

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
                    x = threading.Thread(target=self.amazon_bot, args=(row[2], self.amazon_user, self.amazon_pass, self.amazon_max_price, row[1],))
                elif row[0] == 'newegg':
                    x = threading.Thread(target=self.newegg_bot, args=(row[2], self.newegg_user, self.newegg_pass, row[1],))
                else:
                    self.logger.error('The site "%s" is invalid for row %s. Exiting code. Check the case and spelling of the site.', row[0], row)
                    exit()
                threads.append(x)
                x.start()