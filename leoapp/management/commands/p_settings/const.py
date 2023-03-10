from random import randint
import os

X_FORWARDED = {
    'X - Forwarded - For': f'{randint(1, 255)}.{randint(1, 255)}.{randint(1, 255)}.{randint(1, 255)}, {randint(1, 255)}.{randint(1, 255)}.{randint(1, 255)}.{randint(1, 255)}, {randint(1, 255)}.{randint(1, 255)}.{randint(1, 255)}.{randint(1, 255)}'}

# XML_FILE = f'{os.path.abspath(".")}/sitemap.xml'
XML_FILE = r'leoapp\management\commands\p_settings\sitemap.xml'
DIRECTORY = r'leoapp\management\commands\logs'
DOMAIN = r'https://leonardo.ru'
REG_EXP = r'^https:\/\/leonardo.ru\/ishop\/tree_\/*'
SOUP_ERROR = 'soup_error'
CONNECTION = 'connection'
FILE_ERROR = 'file_error'
