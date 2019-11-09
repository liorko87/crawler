import requests
import lxml.html
import datetime

from db_service import DbService


class PasteBinData:
    def __init__(self, url, username, title, creation_date, content):
        self.url = url
        self.username = username
        self.title = title
        self.creation_date = creation_date
        self.content = content


class DataParser:
    def __init__(self):
        self.db = DbService()

    def parse(self, url):
        try:
            html = requests.get(url)
            doc = lxml.html.fromstring(html.content)
            main_data = doc.xpath('//div[@id="content_left"]')[0]
            
            # parse the title and the username fields
            title = main_data.xpath('//div[@class="paste_box_line1"]')[0].attrib['title']
            user_div = main_data.xpath('//div[@class="paste_box_line2"]/text()')
            str_list = list(filter(None, user_div))
            str_list = [s.rstrip() for s in str_list]
            str_list = list(filter(None, str_list))
            user_name = str_list[0].lower()
            if 'Guest'.lower() in user_name or 'Unknown'.lower() in user_name\
                    or 'Anonymous'.lower() in user_name\
                    or len(user_name) == 0:
                user_name = 'unknown'
            if 'Unknown'.lower() in title or len(title) == 0:
                title = 'unknown'
            
            # parse the date
            date = main_data.xpath('//div[@class="paste_box_line2"]/span')[0].attrib['title'].split(' ')
            date[1] = date[1][:-2]  # remove the `th` ending from the day of the month
            if len(date[1]) == 1:
                date[1] = f'0{date[1]}'  # padding '0' if the day of the month is 1-9
            del date[2]  # remove the 'of' version from the dates list
            date = ' '.join(date)  # cast the dates to string instead of list
            datetime_object = datetime.datetime.strptime(date, '%A %d %B %Y %I:%M:%S %p CDT')

            # parse the content
            content_div = main_data.xpath('//div[@id="selectable"]/ol')[0]
            total_content = []
            for content in content_div:
                total_content.append(content.text_content())

            total_content = ' '.join(total_content).strip() # cast the content to string instead of list

            # create object with all the relevant data
            data = PasteBinData(url, user_name, title, datetime_object, total_content)
            self.db.insert_data(data)

        except IndexError as e:
            print(f'error parsing {url}: {str(e)}\n')
        except UnicodeDecodeError as e:
            print(f'error parsing {url} - unicode does not match utf-8: {str(e)}\n')
            