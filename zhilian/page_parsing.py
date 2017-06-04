import requests
from bs4 import BeautifulSoup
from lxml import etree
import time
import pymongo
import re
import random
from setting import filter_tags
from proxy import proxy_lists

client = pymongo.MongoClient('localhost', 27017)
ceshi = client['zhilian']
item_info = ceshi['item_info']

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Connection':'keep-alive'
}

# proxy_list = [
#     'http://218.56.132.158',
#     'http://115.47.44.102',
#     'http://118.144.149.200',
#     'http://222.223.239.135',
#     'http://123.234.219.133'
# ]
proxy_ip = random.choice(proxy_lists)
proxies = {'http':proxy_ip}

# spider 1
def get_links_from(pages):
    # url_host = 'http://sou.zhaopin.com/jobs/searchresult.ashx?in=210500%3B160400%3B160000%3B160500%3B160200%3B300100%3B160100%3B160600&jl' \
    #       '=上海%2B杭州%2B北京%2B广州%2B深圳&kw="+job+"&p="+x+"&isadv=0'
    channel = 'http://sou.zhaopin.com/jobs/searchresult.ashx?in=210500%3b160400%3b160000%3b160500%3b160200%3b300100%3b160100%3b160600&jl=%e5%85%a8%e5%9b%bd&' \
              'kw=%22+python+%22&sm=0&isfilter=0&fl=489&isadv=0&sb=1&sg=3339e102456541a3adeb312706ea9c54&p='
    list_view = '{}{}/'.format(channel, str(pages))
    try:
        # wb_data = requests.get(list_view, headers=headers, pro)
        wb_data = requests.post(list_view, headers=headers)
        time.sleep(2)
        soup = BeautifulSoup(wb_data.text, 'lxml')
        pattern = re.compile('ssidkey=y&amp;ss=201&amp;ff=03" href="(.*?)" target="_blank"', re.S)  # 正则匹配出招聘信息的URL地址

        if soup.find('table', 'newlist'):
            item_link = re.findall(pattern, wb_data.text)
            # print(item_link)
            for item in item_link:
                get_info(item)
        else:
            # It's the last page !
            pass

    except requests.exceptions.ConnectionError:pass

def get_info(url):

    wb_data = requests.get(url,headers=headers)
    selector = etree.HTML(wb_data.text)
    try:
        title = selector.xpath('//div[@class="inner-left fl"]/h1/text()') #匹配到的职业名称
        mone = selector.xpath('//div[@class="terminalpage clearfix"]/div[@class="terminalpage-left"]/ul[@class="terminal-ul clearfix"]/li[1]/strong/text()')  # 匹配到该职位的月薪
        date = selector.xpath('//div[@class="terminalpage clearfix"]/div[@class="terminalpage-left"]/ul[@class="terminal-ul clearfix"]/li[3]/strong/span/text()')
        adress = selector.xpath('//div[@class="terminalpage clearfix"]/div[@class="terminalpage-left"]/ul[@class="terminal-ul clearfix"]/li[2]/strong/a/text()')  # 匹配工作的地址
        exp = selector.xpath('//div[@class="terminalpage clearfix"]/div[@class="terminalpage-left"]/ul[@class="terminal-ul clearfix"]/li[5]/strong/text()')  # 匹配要求的工作经验
        education = selector.xpath('//div[@class="terminalpage clearfix"]/div[@class="terminalpage-left"]/ul[@class="terminal-ul clearfix"]/li[6]/strong/text()')  # 匹配最低学历
        zhiweileibie = selector.xpath('//div[@class="terminalpage clearfix"]/div[@class="terminalpage-left"]/ul[@class="terminal-ul clearfix"]/li[8]/strong/a/text()')  # 匹配职位类别

        match = re.compile('<!-- SWSStringCutStart -->(.*?)<!-- SWSStringCutEnd -->', re.S)  # 此处为匹配对职位的描述，并且对其结构化处理
        description = re.findall(match, wb_data.text)     # 职位描述
        des = description[0]
        des = filter_tags(des)  # filter_tags此函数下面会讲到
        des = des.strip()
        des = des.replace('&nbsp;', '')
        des = des.rstrip('\n')
        des = des.strip(' \t\n')

        info = {
            'tittle': title,
            'mone': mone,
            'date': date,
            'adress': adress,
            'exp': exp,
            'education': education,
            'zhiweileibie': zhiweileibie,
            'des': des,
            'url': url,
        }
        print(info)
        item_info.insert_one(info)
        print(info)
    except IndexError:
        pass


# get_links_from(2)
# get_info('http://jobs.zhaopin.com/46771761190258576000.htm')
