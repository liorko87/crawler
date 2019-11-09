#!/usr/bin/env python3

import re
import time
import requests
from urllib.parse import urlparse
from parse_data import DataParser


class Crawler:

    def __init__(self, url):
        self.visited = set()
        self.start_url = url
        self.data_parser = DataParser()

    @staticmethod
    def get_html(url):
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
        except requests.exceptions.ConnectionError:
            time.sleep(10)
    
    def start(self):
        self.crawl()
