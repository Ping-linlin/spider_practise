from bs4 import BeautifulSoup
import requests

start_usl = 'http://bj.58.com/sale.shtml'
url_host = 'http://bj.58.com'
def get_channel_urls(url):
    wb_data = requests.get(start_usl)
    soup = BeautifulSoup(wb_data.text, 'lxml')

    links = soup.select('.dlb > a')
    for link in links:
        if link.get('href') == None:
            continue
        else:
            page_url = url_host + link.get('href')
            print(page_url)


get_channel_urls(start_usl)


channel_list = '''

http://bj.58.com/shouji/
http://bj.58.com/tongxunyw/
http://bj.58.com/danche/
http://bj.58.com/zixingche/
http://bj.58.com/diannao/
http://bj.58.com/shuma/
http://bj.58.com/jiadian/
http://bj.58.com/ershoujiaju/
http://bj.58.com/bangong/

http://bj.58.com/fushi/

http://bj.58.com/yishu/

http://bj.58.com/wenti/
http://bj.58.com/chengren/
'''

# http://bj.58.com/yingyou/
# http://bj.58.com/meirong/
# http://bj.58.com/tushu/