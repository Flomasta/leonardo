import os
import re
import requests
from time import sleep
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from defusedxml import ElementTree as ET
from fake_http_header import FakeHttpHeader
from django.core.management.base import BaseCommand

from leoapp.models import Items, ItemProperty, Properties, PriceDynamic
from leoapp.management.commands.p_settings.const import XML_FILE, X_FORWARDED, REG_EXP, DOMAIN, SOUP_ERROR, CONNECTION, \
    FILE_ERROR


#
# from leoapp.management.commands.p_settings.const import X_FORWARDED, XML_FILE, DOMAIN, REG_EXP, SOUP_ERROR, CONNECTION, \
#     FILE_ERROR



# TODO Try except reviev



# check if the size of log file is less than 1mb
def check_log_size(file_path: str) -> str:
    if os.path.exists(file_path):
        file_size = os.path.getsize(file_path)
        # more than 1MB
        if file_size > 999_999:
            return 'w'
    return 'a'


# check if directory exists
def check_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


# append log if file size is less than 1mb or write from the beginning
def logger(filename, ex, directory='logs'):
    check_directory(directory)
    file_path = f'{directory}/{filename}.log'
    idx = check_log_size(file_path)
    with open(file_path, idx, encoding='utf-8') as file:
        now = datetime.now().strftime("%H:%M:%S -- %d-%m-%Y")
        file.write(f'{now} {str(ex)} \n')


# parce xml-file to get sections urls
def get_section_urls(file: str, directory='p_settings') -> list or None:
    lst = []
    try:
        # create element-tree object
        tree = ET.parse(file)
    except OSError as e:
        logger(FILE_ERROR, e)
    else:
        root = tree.getroot()
        for i in root:
            link = i[0].text
            if re.match(REG_EXP, link) and 'filter' not in link:
                lst.append(link)
        return lst


# cook soup from the link
def get_soup(link, timeout=5):
    headers = FakeHttpHeader().as_header_dict()
    headers.update(X_FORWARDED)
    try:
        response = requests.get(link, timeout=timeout, headers=headers)
    except Exception as e:
        logger('connection', e)
    else:
        soup = BeautifulSoup(response.text, 'lxml')
        return soup


# get section url and create list with items url
def get_item_url(soup):
    lst = []
    try:
        data = soup.find_all('div', class_=['goods catalog-goods', 'goods-page-container'])
    except (AttributeError, TypeError) as ex:
        logger(soup, ex)
    else:
        for link in data:
            item_link = link.find('a', class_='goods__link').get('href')
            lst.append(item_link)
        return lst


def get_item_data(location: str):
    url = f'{DOMAIN}{location}'
    url_checker = re.search(r'good|group', url)
    # check if domain has path and web-page works correct
    if not urlparse(url).path or not url_checker:
        return

    try:
        soup = get_soup(url)
    except Exception as e:
        logger(SOUP_ERROR, e)
        return
    else:
        # getting all item features
        item = {'item_id': None,
                'breadcrumbs': None,
                'title': None,
                'description': None,
                'images': None,
                'price': None,
                'url': url
                }
        item_properties = None
        if soup:
            # item_id
            if url_checker:
                item['item_id'] = url.split('_')[-1].strip('/')

            # item_breadcrumbs
            item_breadcrumbs = soup.find_all('a', class_='breadcrumb-link', default=None)
            if item_breadcrumbs:
                item['breadcrumbs'] = '/'.join([i.text for i in item_breadcrumbs])

            # item_title
            item_title = soup.find('h1', class_='card__title', default=None)
            if item_title:
                item['title'] = item_title.text.strip()

            # item_description
            item_description = soup.find('div', 'short-description', default=None)
            if item_description:
                item['description'] = item_description.text

            # item_images
            try:
                item_images = soup.find("div", class_="card__pic").find_all("img", class_='big-image')
            except Exception as ex:
                logger(SOUP_ERROR, ex)
            else:
                if len(item_images) == 1:
                    item['images'] = item_images[0]['src']
                elif len(item_images) > 2:
                    item['images'] = '////'.join([i['src'] for i in item_images])

            # item_price
            item_price = soup.find('p', class_='price', default=None)
            if item_price:
                item['price'] = round(float(item_price.text.strip().split()[0]), 2)

            # item_properties
            reg_exp = r'[^a-zA-Z0-9_А-Яа-яЁё]+'
            it_th = [re.sub(reg_exp, '_', i.text) for i in soup.find_all('div', 'card__about-th', default=None)]
            it_td = [i.text for i in soup.find_all('div', 'card__about-td', default=None)]
            item_properties = dict([i for i in zip(it_th, it_td)])

    return item, item_properties


def fill_table(url):
    # get_data
    item, properties = get_item_data(url)

    # check if data in db

    # fill Items table
    try:
        item_obj = Items.objects.get(item_id=item['item_id'])
        item_obj.item_id = item['item_id']
        item_obj.title = item['title']
        item_obj.price = item['price']
        item_obj.item_url = item['url']
        item_obj.images = item['images']
        item_obj.description = item['description']
        item_obj.breadcrumbs = item['breadcrumbs']
        item_obj.save()
    except Items.DoesNotExist:
        item_obj = Items(
            item_id=item['item_id'],
            title=item['title'],
            price=item['price'],
            item_url=item['url'],
            images=item['images'],
            description=item['description'],
            breadcrumbs=item['breadcrumbs']
        )
        item_obj.save()

    # fill table PriceDynamic
    p_d = PriceDynamic(item_id=item_obj, item_price=item_obj.price,
                       price_date=datetime.now())
    p_d.save()

    # fill table Properties and ItemProperty
    for k, v in properties.items():
        try:
            p = Properties.objects.get(property_name=k)
            item_prop_value = ItemProperty.objects.filter(property_id_id=p, item_id_id=item_obj).exists()
            if not item_prop_value:
                item_prop_value = ItemProperty(property_value=v, property_id=p, item_id=item_obj)
                item_prop_value.save()
        except:
            p = Properties(property_name=k)
            p.save()
            p = Properties.objects.get(property_name=k)
            item_prop_value = ItemProperty(property_value=v, property_id=p, item_id=item_obj)
            item_prop_value.save()


def main():
    if get_section_urls(XML_FILE):
        sections = get_section_urls(XML_FILE)
        # get single section url
        for section in sections:
            soup = get_soup(section)
            items_urls = get_item_url(soup)
            # get single item url
            print(items_urls)
            if items_urls:
                for item_url in items_urls:
                    print(section)
                    print(f'{DOMAIN}{item_url}')
                    fill_table(item_url)
                    # sleep(0.3)


class Command(BaseCommand):
    help = 'Scrapper for leonardo.ru'

    def handle(self, *args, **options):
        main()
        # print('hi')
