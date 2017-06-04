import time
from page_parsing import url_list
from page_parsing import item_info

while True:
    print(url_list.find().count())
    time.sleep(5)


# while True:
#     print(item_info.find().count())
#     time.sleep(5)