import os
import shutil
import unittest
from bs4 import BeautifulSoup
from management.commands.settings.const import DOMAIN
from management.commands.leo_scrapper import check_log_size, logger, get_soup, get_section_urls, get_item_url


class CheckLogSizeTest(unittest.TestCase):

    def test_check_log_size(self):
        file_path = 'test.txt'
        # Create a 1MB file
        with open(file_path, 'w') as f:
            f.write('x' * 1000000)
        self.assertEqual(check_log_size(file_path), 'w')

        # Create a 0.5MB file 
        with open(file_path, 'w') as f:
            f.write('x' * 500000)

        self.assertEqual(check_log_size(file_path), 'a')


class LoggerTest(unittest.TestCase):
    def test_logger(self):
        filename = "test"
        ex = "This is a test exception"
        logger(filename, ex)

        logfile = f"logs/{filename}.log"

        self.assertTrue(os.path.exists(logfile))

        with open(logfile, "r") as f:
            content = f.read()  # read contents of the log file
            self.assertIn(ex, content)

    def tearDown(self):
        os.remove('test.txt')
        # remove all the files in the directory and the directory itself
        shutil.rmtree('logs')


class TestGetSectionUrls(unittest.TestCase):

    def test_valid_file(self):
        # create a sample XML file
        xml_str = '''<?xml version="1.0"?>
    <root>
        <item>
            <link>https://leonardo.ru/ishop/tree_9538925500/</link>
        </item>
        <item>
            <link>https://leonardo.ru/ishop/tree_9538924784/?filter=tiptovara:856</link>
        </item>
        <item>
            <link>https://leonardo.ru/educational-program/</link>
        </item>
        <item>
            <link>https://leonardo.ru/sertificat/plastic/</link>
        </item>
        <item>
            <link>https://leonardo.ru/masterclasses/novorossiysk/novorossiysk/</link>
        </item>
    </root>'''
        with open('test_file.xml', 'a') as f:
            f.write(xml_str)

        # call the function and check the result
        result = get_section_urls('test_file.xml')
        expected = ['https://leonardo.ru/ishop/tree_9538925500/']
        self.assertEqual(result, expected)

    def test_invalid_file(self):
        result = get_section_urls('non_existent_file.xml')
        self.assertIsNone(result)

    def tearDown(self):
        if os.path.exists('test_file.xml'):
            os.remove('test_file.xml')


class GetSoupTest(unittest.TestCase):

    def test_get_soup(self):
        soup = get_soup(DOMAIN)
        self.assertIsInstance(soup, BeautifulSoup)

    def test_get_soup_invalid_link(self):
        invalid_link = 'http://invalid.com'
        self.assertEqual(get_soup(invalid_link), None)

    def test_get_soup_timeout(self):
        self.assertEqual(get_soup(DOMAIN, 0.1), None)


class GetItemUrlTest(unittest.TestCase):
    def test_valid_soup(self):
        # Create a sample soup object
        sample_html = '''
        <div class="goods catalog-goods">
            <a class="goods__link" href="/item1"></a>
            <a class="goods__link" href="/item2"></a>
        </div>
        <div class="goods-page-container">
            <a class="goods__link" href="/item3"></a>
            <a class="goods__link" href="/item4"></a>
        </div>
        '''
        soup = BeautifulSoup(sample_html, 'lxml')

        # Call the function and check the result
        result = get_item_url(soup)
        self.assertEqual(result, ['/item1', '/item3'])

    def test_invalid_soup(self):
        # Pass in None as the soup argument
        result = get_item_url(None)

        # Check that the function returns None
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
