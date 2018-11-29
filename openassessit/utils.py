import time
import re

def generate_img_filename(url, identifier):
    """generate useful filename with a max of 150 chars"""
    return re.sub(r'\W', '-', '%s%s' % (url[0:40], identifier[-110:])) + '.png'


def scroll_down(driver, value):
    """ Scroll down some """
    driver.execute_script("window.scrollBy(0,"+str(value)+")")


def detect_full_html_loaded(driver):
    """ Keep scrolling until DOM is done changing """
    n = 10
    old_html = driver.page_source
    while n > 0:
        for i in range(2):
            print('Waiting for DOM and ajaxy stuff to load...')
            scroll_down(driver, 1000)
            time.sleep(2)
            n = n-1
        new_html = driver.page_source
        if new_html != old_html:
            old_html = new_html
        else:
            print('DOM is sufficently loaded.')
            break

    return True