from bs4 import BeautifulSoup
import requests
import time
import pymongo

client = pymongo.MongoClient('localhost', 27017)
ceshi = client['ceshi']
url_list = ceshi['url_list2']
item_info = ceshi['item_info2']


# spider 1
def get_links_from(channel, pages, who_sells=0):
    # http://bj.58.com/bangong/1/pn2/
    list_view = '{}{}/pn{}'.format(channel, str(who_sells), str(pages))
    wb_data = requests.get(list_view)
    time.sleep(4)
    soup = BeautifulSoup(wb_data.text, 'lxml')

    if soup.find('td', 't'):
        for link in soup.select('td.t a.t'):
            item_link = link.get('href').split('?')[0]
            url_list.insert_one({'url': item_link})
            print(item_link)
    else:
        pass

# spider 2
def get_item_info(url):
    wb_data = requests.get(url)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    no_longer_exist = '404' in soup.find('script', type="text/javascript").get('src').split('/')
    if no_longer_exist:
        pass
    else:
        title = soup.title.text
        # price = soup.select('span.price.c_f50')[0].text.strip().lstrip().rstrip(',') if soup.find_all('span.price.c_f50') else soup.select('span.price_now > i')[0].text
        price = soup.select('span.price.c_f50')[0].text.strip().lstrip().rstrip(',')
        date = soup.select('.time')[0].text
        area = list(soup.select('.su_con a')[0].stripped_strings) if soup.find_all('div', 'su_con') else None
        # 三目运算

        item_info.insert_one({'title': title, 'price': price, 'date': date, 'area': area})
        # print({'title': title, 'price': price, 'date': date, 'area': area})

# get_item_info('http://bj.58.com/tongxunyw/29990877178035x.shtml')