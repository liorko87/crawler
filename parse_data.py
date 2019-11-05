import requests
import lxml.html


def main():
    html = requests.get('https://pastebin.com/SqqZXnBg')
    doc = lxml.html.fromstring(html.content)
    main_data  = doc.xpath('//div[@id="content_left"]')[0]
    title_div = main_data.xpath('//div[@class="paste_box_line1"]')[0].attrib['title']
    user_div = main_data.xpath('//div[@class="paste_box_line2"]/text()')
    str_list = list(filter(None, user_div))
    str_list = [s.rstrip() for s in str_list]
    str_list = list(filter(None, str_list))
    user_name = str_list[0]
    date = main_data.xpath('//div[@class="paste_box_line2"]/span')[0].attrib['title']
    print(title_div, date, user_name)


    #parse the content

    content_div = main_data.xpath('//div[@id="selectable"]/ol')[0]
    total_content = []
    for content in content_div:
        total_content.append(content.text_content())
    
    print(total_content)



if __name__ == "__main__":
    main()


# https://pythontips.com/2018/06/20/an-intro-to-web-scraping-with-lxml-and-python/