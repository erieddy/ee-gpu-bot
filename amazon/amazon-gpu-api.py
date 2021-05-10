import time
import re
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import sys, getopt


def main(argv):
    loginPassword = ''
    loginUsername = ''
    varCount = 0 
    try: 
        opts, args = getopt.getopt(argv,"hp:u:",["password=","username="])
    except getopt.GetoptError:
        print('amazon-gpu.py [-u | --username] <username> [-p | --password] <password>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('Help - Run using the following required parameters')
            print('amazon-gpu.py [-u | --username] <username> [-p | --password] <password>')
            sys.exit()
        elif opt in ("-p", "--password"):
            loginPassword = arg
            varCount = varCount + 1
        elif opt in ("-u", "--username"):
            varCount = varCount + 1
            loginUsername = arg
    if(varCount == 2):
        print('Paramters are good')
        order(loginPassword, loginUsername)
    else:
        print('Input the required fields')
        print('amazon-gpu.py [-u | --username] <username> [-p | --password] <password>')


def order(loginPassword,loginUsername):
    #Create log
    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S')

    #logging.basicConfig(filename='.log', encoding='utf-8', level=logging.DEBUG)


    #Start browser
    #change this based on your path for your Chrome driver. Download your chrome driver here https://chromedriver.chromium.org/downloads
    browser = webdriver.Chrome('/Users/eric/Documents/chromedriver')

    #amazon login
    browser.get('https://www.amazon.com/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2Fref%3Dnav_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=usflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&')

    #fill in email
    emailField = browser.find_element_by_name('email')
    emailField.send_keys(loginUsername)

    #continue top next step
    contineButon = browser.find_elements_by_class_name('a-button-input')
    contineButon[0].click()

    #input password
    passwordField = browser.find_elements_by_id('ap_password')
    passwordField[0].send_keys(loginPassword)

    try:
        #click sign in
        signInButton = browser.find_elements_by_id('signInSubmit')
        signInButton[0].click()
    except:
        logging.error('Failed to find the ')

    temp = ['https://www.amazon.com/XFX-Speedster-QICK319-Graphics-RX-67XTYLUDP/dp/B08YKH7VMN/?_encoding=UTF8&pd_rd_w=7BLI1&pf_rd_p=49ff6d7e-521c-4ccb-9f0a-35346bfc72eb&pf_rd_r=VDTB0F1VTNQTN7NM6CJ0&pd_rd_r=f02ed5ff-5a5d-475c-8606-c249e6c712c9&pd_rd_wg=Ut65g&ref_=pd_gw_ci_mcx_mr_hp_d']

    ##change the links here for the items you want to watch
    rtx3080 = ['https://www.amazon.com/dp/B08HH5WF97',
    'https://www.amazon.com/dp/B08J6F174Z',
    'https://www.amazon.com/Gaming-GeForce-Graphics-DisplayPort-Bearings/dp/B08TFLDLTM/ref=sr_1_1?dchild=1&keywords=rtx+3080+tuf&qid=1618544089&sr=8-1',
    'https://www.amazon.com/dp/B08HR3Y5GQ/?coliid=I1KNOLQ85AEV6H&colid=3CSHWUEOMDZSG&psc=0&ref_=lv_ov_lig_dp_it',
    'https://www.amazon.com/dp/B08J6F174Z/?coliid=I1LA5GPTCI290E&colid=3CSHWUEOMDZSG&psc=0&ref_=lv_ov_lig_dp_it']

    checkingStock = True

    while checkingStock:
        logging.debug('starting while loop')
        for i in rtx3080:
            print('Starting for loop')
            browser.get(i)

            #time.sleep(1)
            try:

                #look for add to cart and click
                addToCart = browser.find_element_by_id('add-to-cart-button')
            except: 
                logging.debug("Couldn't find the add to cart button item must be out of stock. Moving to next item")
                #Sleeping for 2 seconds before moving to next item
                browser.find_element_by_id('nav-hamburger-menu').click()

                time.sleep(2)
                continue

            #find ASIN
            logging.debug('Finding ASIN')
            asinCodeTemp = re.findall("B0[A-Z,0-9]\w+", i)
            asinCode = asinCodeTemp[0]
            asinCode = asinCode.strip()
            logging.debug('ASIN code is "' + asinCode +'".')
            url = 'https://www.amazon.com/gp/aws/cart/add.html?AssociateTag=brobot02-20&AWSAccessKeyId=AKIAIVQ27DOD3FLEYHJA&Quantity.1=1&ASIN.1=' + asinCode
            logging.debug('clicking link ' + url)
                
            #time.sleep(2)
            try:
                browser.get(url)
            except: 
                logging.error('Failed to click Assoicate item URL')
            
            logging.debug('done adding to cart')
            #https://www.amazon.com/gp/aws/cart/add.html?AssociateTag=brobot02-20&AWSAccessKeyId=AKIAIVQ27DOD3FLEYHJA&Quantity.1=1&ASIN.1=B08YKH7VMN

            #time.sleep(2)
            try:
                browser.find_element_by_name('add').click()
            except:
                logging.error('Failed to click add to cart button')
            checkingStock = False
            break
            #time.sleep(2)
            

    logging.debug('ending while loop')


    #moving to checkout
    #time.sleep(2)
    logging.debug('Moving to cart')
    try:
        browser.find_element_by_name('proceedToRetailCheckout').click()
    except:
        logging.error("Can't find move to cart button")


    #place order
    try:
        logging.debug('Clicking the checkout button')
        browser.find_element_by_name('placeYourOrder1').click()

    except:
        logging.error('Failed to click place order')

if __name__ == "__main__":
   main(sys.argv[1:])