from selenium import webdriver
from PIL import Image,ImageDraw
from io import BytesIO
import time
import re
import argparse
import os
import json
import sys
import logging
from .utils import initialize_logger, generate_img_filename, scroll_down, detect_full_html_loaded
from .templates import template_path

def get_args():
    example_text = '''
    examples:

    python -m openassessit.capture --input-file="/abs/path/to/lighthouse-report.json" --assets-dir="/abs/path/to/assets" --sleep=1 --driver=firefox

    '''

    parser = argparse.ArgumentParser(epilog=example_text, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i', '--input-file', help='Use absolute path to the lighthouse json report')
    parser.add_argument('-a', '--assets-dir', help='Use absolute path to /assets dir')
    parser.add_argument('-s', '--sleep', type=float, help='Number of seconds to wait before taking screenshots')
    parser.add_argument('-d', '--driver', choices=['firefox', 'chrome'], help='Name of the webdriver.')
    return parser.parse_args()


def get_firefox_driver():
    """ Get Firefox driver """
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')
    options.add_argument('--window-size=1400,800')
    return webdriver.Firefox(options=options)


def get_chrome_driver():
    """ Get Chrome driver """
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--window-size=1400,800')
    options.add_argument("--disable-device-emulation")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--force-device-scale-factor=1")
    return webdriver.Chrome(options=options)


def create_backup_image(assets_dir, elem_identifier, elem_image_name):
    """ Create fallback image """
    im = Image.new('RGB', (300, 50), color = (255,182,193))
    ImageDraw.Draw(im).text((20,20), 'Image could not be created. See Console.', fill=(0,0,0))
    im.save(os.path.join(assets_dir,elem_image_name))
    # try:
    #     im.save(os.path.join(assets_dir,elem_image_name))
    # except:
    #     im.save(os.path.join(assets_dir,'no-image.png'))
    #     logging.warning('Skiping element: "%s" because: %s' % (elem_identifier))


def capture_screenshot(assets_dir, url, sleep, driver):
    """ Take simple screenshot of above-the-fold """
    try:
        driver.get(url)
        time.sleep(sleep)
        driver.set_window_size(1400, 700)
        im = Image.open(BytesIO(driver.get_screenshot_as_png()))
        im = im.resize([int(0.35 * s) for s in im.size], Image.ANTIALIAS)
        # im.save(os.path.join(assets_dir,'screenshot.png'))
        # logging.info('Created: screenshot.png')
        shot_name = generate_img_filename(url, 'cat', '_screenshot_')
        print(shot_name)
        im.save(os.path.join(assets_dir,shot_name))
        logging.info('Created: ' + shot_name)
    except Exception as ex:
        logging.warning('Skipping element "%s" because: %s' % (url, ex))
        logging.debug(ex)


def capture_element_pic(input_file, assets_dir, url, elem_identifier, lhIdee, sleep, driver):
    """ Capture image of element and save """
    try:
        driver.get(url)
        driver.set_window_size(1400, driver.execute_script("return document.body.parentNode.scrollHeight"))
        elem = driver.find_element_by_css_selector(elem_identifier) # find element
        location = elem.location
        size = elem.size
        elem_image_name = generate_img_filename(url, elem_identifier, lhIdee)

        if (size == {'height': 0.0, 'width': 0.0}):
            create_backup_image(assets_dir, elem_identifier, elem_image_name)
            logging.warning('Skipping element because the element is invisible or has height and width of zero.')
        elif not location:
            create_backup_image(assets_dir, elem_identifier, elem_image_name)
            logging.warning('Skipping element because the webdriver could not locate the element to create image.')
        else:
            im = Image.open(BytesIO(driver.get_screenshot_as_png())) # uses PIL library to open image in memory
            im = im.crop((location['x'] -4,
                        location['y'] -4,
                        location['x'] + size['width'] +8,
                        location['y'] + size['height'] +8
                        ))
            im.save(os.path.join(assets_dir,elem_image_name)) # saves new cropped image
            logging.info('Created: %s' % (elem_image_name))
            if im.convert("L").getextrema() == (0, 0): # check if image is white
                create_backup_image(assets_dir, elem_identifier, elem_image_name)
                logging.warning('%s image was all white and not a useful image.' % (elem_image_name))
    except Exception as ex:
        logging.warning('Skipping element "%s" because: %s:' % (elem_identifier, ex))
        logging.debug(ex)
        pass


def identifier_generator(data, *auditref_whitelist):
    """ Create and yield each elements selector when it is in the audit whitelist """
    for sel in auditref_whitelist:
        audit = data.get('audits', {}).get(sel)

        if audit is None:
            logging.error("Invalid audit id: %s" % sel)
            continue

        for item in audit.get('details', {}).get('items', []):
            if item['node']['selector'] == ':root':
                logging.warning('Selector returned as ":root", no image will be created.') # If Axe returns ":root" it does not create a helpful screenshot
            else:
                yield item['node']['selector'], item['node']['lhId']


def main():
    """ Parse Lighthouse JSON for failing elements and capture images of those elements """
    args = get_args()
    input_file = args.input_file
    assets_dir = args.assets_dir
    output_dir = os.path.dirname(args.input_file)
    sleep = args.sleep
    initialize_logger('capture', output_dir)
    logging.info('Starting image creation...')
    if args.driver == 'firefox':
        driver = get_firefox_driver()
    elif args.driver == 'chrome':
        driver = get_chrome_driver()
    else:
        raise ValueError("Driver must be one of: firefox, chrome")
    try:
        with open(input_file, encoding='utf-8') as json_file:
            data = json.load(json_file)
            detect_full_html_loaded(driver)
            capture_screenshot(assets_dir, data['finalUrl'], sleep, driver)
        for sel,lhIdee in identifier_generator(data, 'color-contrast', 'link-name', 'button-name', 'image-alt', 'input-image-alt', 'label', 'accesskeys', 'frame-title', 'list', 'listitem', 'definition-list', 'dlitem', 'aria-allowed-attr', 'aria-required-attr', 'aria-required-children', 'aria-required-parent', 'aria-roles', 'aria-valid-attr-value', 'aria-valid-attr'):
            capture_element_pic(input_file, assets_dir, data['finalUrl'], sel, lhIdee, sleep, driver)
    finally:
        driver.quit()
        logging.info('Image creation complete in: "%s"' % (assets_dir))


if __name__ == '__main__':
    main()
