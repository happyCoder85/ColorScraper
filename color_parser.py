"""
Description: Class that parses HTML color data from https://www.colorhexa.com/color-names
Author: Jonathan Spurling
Section Number: ADEV-3005(251409)
Date Created: March 11, 2024

Updates: March 14, 2024
"""
from html.parser import HTMLParser
from urllib.error import URLError
import urllib.request
from pprint import pprint


class ColorParser(HTMLParser):
    """ Class to parse html data from a webpage."""
    def __init__(self,*, convert_charrefs: bool = ...) -> None:
        """ Initializes a MyHTMLParser instance"""
        super().__init__(convert_charrefs=convert_charrefs)
        self.td = False
        self.a = False
        self.colour = ''
        self.count = 0
        self.colours = {}

    def handle_starttag(self, tag, attrs):
        """ Finds the td/a start tags"""
        if tag == 'td':
            self.td = True
        if self.td and tag == 'a':
            self.a = True
        #for attr in attrs:
         #  print("     attr:", attr)

    def handle_endtag(self, tag):
        """ Finds the td/a tag end tags"""
        if tag == 'td':
            self.td = False
        if self.td and tag == 'a':
            self.a = False

    def handle_data(self, data):
        """ Handles the data that is obtained inside the td/a tags"""
        if self.td and self.a:
            self.count += 1
            if self.count % 2 != 0:
                self.colour = data
            else:
                self.colours[self.colour] = data
        return self.colours

    def count_data(self):
        """ Returns the count total for all the colours"""
        return self.count / 2

myparser = ColorParser()

try:
    with urllib.request.urlopen('https://www.colorhexa.com/color-names') as response:
        HTML = str(response.read())
        myparser.feed(HTML)
except URLError as e:
    print(f"Failed to retrieve data: {e.reason}")
pprint(myparser.colours)

print(f"Total colours: {int(myparser.count_data())}")
