import requests
import lxml.html
import datetime


class DataParser:
    def __init__(self):
        pass
    
    def parse(self, url):
        try:
            html = requests.get(url)
            doc = lxml.html.fromstring(html.content)
            main_data = doc.xpath('//div[@id="content_left"]')[0]
            title = main_data.xpath('//div[@class="paste_box_line1"]')[0].attrib['title']
            user_div = main_data.xpath('//div[@class="paste_box_line2"]/text()')
            str_list = list(filter(None, user_div))
            str_list = [s.rstrip() for s in str_list]
            str_list = list(filter(None, str_list))
            user_name = str_list[0].lower()
            if 'Guest'.lower() in user_name or 'Unknown'.lower() in user_name or 'Anonymous'.lower() in user_name\
                    or len(user_name) == 0:
                user_name = 'unknown'
            if 'Unknown'.lower() in title or len(title) == 0:
                title = 'unknown'
            date = main_data.xpath('//div[@class="paste_box_line2"]/span')[0].attrib['title'].split(' ')
            date[1] = date[1][:-2]
            if len(date[1]) == 1:
                date[1] = f'0{date[1]}'
            del date[2]
            date = ' '.join(date)
            datetime_object = datetime.datetime.strptime(date, '%A %d %B %Y %I:%M:%S %p CDT')
            print(title, date, user_name)

            # parse the content
            content_div = main_data.xpath('//div[@id="selectable"]/ol')[0]
            total_content = []
            for content in content_div:
                total_content.append(content.text_content())

            print(total_content)

        except IndexError as e:
            with open('errorLog.log', 'a+') as error_log:
                error_log.write(f'error parsing {url}: {e.message}\n')


def main():
    p = DataParser('https://pastebin.com/SqqZXnBg')
    p.parse()


if __name__ == "__main__":
    main()


# https://pythontips.com/2018/06/20/an-intro-to-web-scraping-with-lxml-and-python/