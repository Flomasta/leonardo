from random import randint

X_FORWARDED = {
    'X - Forwarded - For': f'{randint(1, 255)}.{randint(1, 255)}.{randint(1, 255)}.{randint(1, 255)}, {randint(1, 255)}.{randint(1, 255)}.{randint(1, 255)}.{randint(1, 255)}, {randint(1, 255)}.{randint(1, 255)}.{randint(1, 255)}.{randint(1, 255)}'}

XML_FILE = 'leoapp/management/commands/p_settings/sitemap.xml'
DOMAIN = 'https://leonardo.ru'
REG_EXP = '^https:\/\/leonardo.ru\/ishop\/tree_\/*'
SOUP_ERROR = 'soup_error'
CONNECTION = 'connection'
FILE_ERROR = 'file_error'
