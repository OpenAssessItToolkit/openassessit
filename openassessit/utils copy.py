import time
import re
import logging
import os.path
import argparse
import string
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys



def initialize_logger(module, output_dir):
    """ Configure logging """
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    # create console handler and set level to info
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    # create debug file handler and set level to debug
    handler = logging.FileHandler(os.path.join(output_dir, 'log-' + module + '.log'),'w')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def generate_img_filename(url, identifier, lhIdee):
    """ Generate useful filename with a max of 260 chars """
    url = re.sub(r"https?://(www\.)?", '', url)
    identifier = re.sub(r'\W+', '-', identifier)
    return re.sub(r'\W+', '-', '%s%s%s' % (url[0:100], identifier[-100:0], lhIdee)) + '.png'


def scroll_down(driver):
    print('started scroll_down')
    """ Scroll down some by sending a spacebar action"""
    elm = driver.find_element(By.CSS_SELECTOR, "html")
    for _ in range(4):
        elm.send_keys(Keys.SPACE)
        elm.send_keys(Keys.END)
        # time.sleep(0.250)
        print('Scrolling down...')

    # time.sleep(1)
    # actions = ActionChains(driver)
    # for _ in range(4):
    #     actions.send_keys(Keys.SPACE).perform()
    #     time.sleep(1)
        
    # driver.execute_script("window.scrollBy(0,"+str(value)+")")


# def scroll_down(driver):
#     """A method for scrolling the page."""

#     # Get scroll height.
#     last_height = driver.execute_script("return document.body.scrollHeight")
#     print(last_height)

#     while True:

#         # Scroll down to the bottom.
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

#         # Wait to load the page.
#         time.sleep(5)

#         # Calculate new scroll height and compare with last scroll height.
#         new_height = driver.execute_script("return document.body.scrollHeight")
#         print(new_height)

#         if new_height == last_height:

#             break

#         last_height = new_height

# def scroll_down(driver):
#     scroll_pause_time = 3 # You can set your own pause time. My laptop is a bit slow so I use 1 sec
#     screen_height = driver.execute_script("return window.screen.height;")   # get the screen height of the web
#     i = 1

#     while True:
#         # scroll one screen height each time
#         driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
#         i += 1
#         time.sleep(scroll_pause_time)
#         # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
#         scroll_height = driver.execute_script("return document.documentElement.scrollHeight;")  
#         print(scroll_height)
#         print(screen_height)
#         # Break the loop when the height we need to scroll to is larger than the total scroll height
#         if (screen_height) * i > scroll_height:
#             break


def detect_full_html_loaded(driver):
    """ Keep scrolling until DOM is done changing """
    print('started detect_full_html_loaded')
    n = 2
    old_html = driver.page_source
    print('pre scroll down')
    scroll_down(driver)
    print('post scroll down')
    while n > 0:
        for i in range(2):
            logging.info('Waiting for DOM and ajaxy stuff to load...')
            scroll_down(driver)
            # time.sleep(0.250)
            n = n-1
        new_html = driver.page_source
        if new_html != old_html:
            old_html = new_html
        else:
            logging.info('DOM is sufficently loaded.')
            break
    return True


class readable_dir(argparse.Action):
    """ Add an option for readable directories for argparse https://bit.ly/2FBplyx """
    def __call__(self, parser, namespace, values, option_string=None):
        prospective_dir = values
        if not os.path.isdir(prospective_dir):
            raise argparse.ArgumentTypeError(
               "readable_dir:{0} is not a valid path".format(prospective_dir)
            )
        if os.access(prospective_dir, os.R_OK):
            setattr(namespace, self.dest, prospective_dir)
        else:
            raise argparse.ArgumentTypeError(
                "readable_dir:{0} is not a readable dir".format(
                    prospective_dir)
            )
