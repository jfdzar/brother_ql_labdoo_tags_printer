import json
import logging
import subprocess
import time

import urllib.request
from urllib.request import urlopen
from bs4 import BeautifulSoup

from PIL import Image, ImageDraw, ImageFont


def read_battery_capacity(tag):
    try:
        url = 'https://www.labdoo.org/content/tag-one-dooject?id=0000'+tag
        html = urlopen(url)
        html_soup = BeautifulSoup(html, 'html.parser')

        bat_cap = str(html_soup)[str(html_soup).find(
            'watt-hours:')+16:str(html_soup).find("watt-hours:")+20]

        if bat_cap == "Not ":
            bat_cap = "Not Available"
        else:
            bat_cap = bat_cap + " Wh"

        return bat_cap
    except Exception as e:
        logging.error("Error Reading Battery Capacity")
        logging.error(e)
        return ""


def read_save_qr_code(tag):
    try:
        qr_add = "https://api.qrserver.com/v1/create-qr-code/?"
        qr_add = qr_add+"size=180x180&data=http%3A%2F%2Fwww.labdoo.org%2Flaptop%2F0000"
        urllib.request.urlretrieve(
            qr_add+tag, "img/qr.png")
    except Exception as e:
        logging.error("Error Reading QR Code")
        logging.error(e)


def create_device_label(tag):
    try:
        filename = "img/device_tag.png"

        img = Image.new('RGB', (554, 200), color=(255, 255, 255))

        fnt = ImageFont.truetype(
            '/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 30)
        d = ImageDraw.Draw(img)
        d.text((10, 70), "Device Tag ID:", font=fnt, fill=(0, 0, 0))
        d.text((10, 105), "000"+tag, font=fnt, fill=(0, 0, 0))

        fnt = ImageFont.truetype(
            '/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 14)
        d.text((10, 140), "This device has to stay at your property",
               font=fnt, fill=(0, 0, 0))
        d.text((10, 165), "or donations will stop", font=fnt, fill=(0, 0, 0))

        im_qr = Image.open('img/qr.png')
        im_logo = Image.open('logo.png')
        img.paste(im_qr, (360, 10))
        img.paste(im_logo.resize((210, 55)), (5, 5))
        img.save(filename)

        return filename
    except Exception as e:
        logging.error("Error Reading Creating Label")
        logging.error(e)
        return ""


def create_power_adaptor_label(tag):
    try:
        filename = "img/power_tag.png"
        img = Image.new('RGB', (554, 200), color=(255, 255, 255))

        fnt = ImageFont.truetype(
            '/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 30)
        d = ImageDraw.Draw(img)
        d.text((10, 70), "Power Adap.Tag ID:", font=fnt, fill=(0, 0, 0))
        d.text((10, 105), "000"+tag, font=fnt, fill=(0, 0, 0))

        im_qr = Image.open('img/qr.png')
        im_logo = Image.open('logo.png')
        img.paste(im_qr, (360, 10))
        img.paste(im_logo.resize((210, 55)), (5, 5))
        img.save(filename)

        return filename
    except Exception as e:
        logging.error("Error Reading Creating Label")
        logging.error(e)
        return ""


def create_battery_label(tag, bat_cap):
    try:
        filename = "img/battery_tag.png"
        img = Image.new('RGB', (554, 200), color=(255, 255, 255))

        fnt = ImageFont.truetype(
            '/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 30)
        d = ImageDraw.Draw(img)
        d.text((10, 70), "Battery Comp. ID:", font=fnt, fill=(0, 0, 0))
        d.text((10, 105), "000"+tag, font=fnt, fill=(0, 0, 0))

        fnt = ImageFont.truetype(
            '/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 20)
        d.text((10, 140), "Battery Watt-Hours", font=fnt, fill=(0, 0, 0))
        d.text((10, 165), bat_cap, font=fnt, fill=(0, 0, 0))

        im_qr = Image.open('img/qr.png')
        im_logo = Image.open('logo.png')
        img.paste(im_qr, (360, 10))
        img.paste(im_logo.resize((210, 55)), (5, 5))
        img.save(filename)

        return filename
    except Exception as e:
        logging.error("Error Reading Creating Label")
        logging.error(e)
        return ""


def save_tag_images(tag):
    """
    Function to look in labdoo.org for a tag and
    create the images of the labels
    """
    read_save_qr_code(tag)
    bat_cap = read_battery_capacity(tag)

    device_img = create_device_label(tag)
    power_adaptor_img = create_power_adaptor_label(tag)
    battery_img = create_battery_label(tag, bat_cap)

    img_files = [device_img, power_adaptor_img, battery_img]

    return img_files


def print_label(img_file, model, printer):
    """
    Given a image file print the label
    """
    bashCommand = "brother_ql -m "+model+" -p "+printer+" print -l 50 "+img_file
    process = subprocess.Popen(
        bashCommand.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()

    logging.info(output.decode('utf-8'))
    logging.error(error.decode('utf-8'))

    #input("Press any key to continue next image")
    time.sleep(5)


if __name__ == '__main__':

    logging.basicConfig(
        format="%(asctime)s: %(message)s",
        # filemode='a',
        # filename='HA-Watch.log',
        level=logging.INFO,
        datefmt="%H:%M:%S")

    # Read Printer Configuration File
    with open('config.json', 'r') as f:
        printer_config = json.load(f)

    logging.info(printer_config['printer'])
    logging.info(printer_config['model'])

    # Read Tags
    labdoo_tags = []
    with open('tags.txt', 'r') as f:
        labdoo_tags = f.readlines()

    for tag in labdoo_tags:

        # Read the website tag and create images
        img_files = save_tag_images(tag)

        if not img_files:
            continue

        # Print the Labels
        for img in img_files:
            print_label(img, printer_config['model'],
                        printer_config['printer'])
