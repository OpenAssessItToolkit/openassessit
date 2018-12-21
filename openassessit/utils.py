import time
import re
import logging
import os.path


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


def generate_img_filename(url, identifier):
    """ Generate useful filename with a max of 260 chars """
    return re.sub(r'\W', '-', '%s%s' % (url[0:36], identifier[-210:])) + '.png'


def scroll_down(driver, value):
    """ Scroll down some """
    driver.execute_script("window.scrollBy(0,"+str(value)+")")


def detect_full_html_loaded(driver):
    """ Keep scrolling until DOM is done changing """
    n = 10
    old_html = driver.page_source
    while n > 0:
        for i in range(2):
            logging.info('Waiting for DOM and ajaxy stuff to load...')
            scroll_down(driver, 1000)
            time.sleep(2)
            n = n-1
        new_html = driver.page_source
        if new_html != old_html:
            old_html = new_html
        else:
            logging.info('DOM is sufficently loaded.')
            break

    return True