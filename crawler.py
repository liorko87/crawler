#!/usr/bin/env python3

"""
import requests
from lxml import etree
from io import StringIO
import tinydb
import arrow
import urllib
"""

import re
import requests
from lxml import html
from urllib.parse import urlparse
from parse_data import DataParser


class Crawler():

    def __init__(self):
        self.visited = set()
        self.start_url = 'https://pastebin.com/archives'
        self.data_parser = DataParser()

    
    def get_html(self, url):
        try:    
            html = requests.get(url)    
        except Exception as e:    
            print(e)    
            return ""    
        return html.content.decode('utf_8')

    def get_links(self):
        raw_html = self.get_html(self.start_url)
        parsed = urlparse(self.start_url)
        base = f"{parsed.scheme}://{parsed.netloc}"
        links = re.findall(r'''<a\s+(?:[^>]*?\s+)?href="([^"]*)"''', raw_html)
        
        for idx, link in enumerate(links):
            if urlparse(link):
                link_with_base = base + link
                links[idx] = link_with_base

        return set(filter(lambda x: 'mailto' not in x, links))

    """ def extract_info(self, link):
        html = self.get_html(link)
        meta = re.findall("<meta .*?name=[\"'](.*?)['\"].*?content=[\"'](.*?)['\"].*?>", html)    
        return dict(meta) """

    def crawl(self):
        try:
            links = self.get_links()
            for link in links:
                if link in self.visited:
                    continue
                self.visited.add(link)
                self.data_parser.parse(link)
                self.crawl()
        except KeyboardInterrupt:
            print('Crawler cancelled by the user')
    
    def start(self):
        self.crawl()



def main():
    crawler = Crawler()
    crawler.start()


if __name__ == "__main__":
    main()

#https://dev.to/fprime/how-to-create-a-web-crawler-from-scratch-in-python-2p46