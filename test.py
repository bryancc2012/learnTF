# 此段代码用于从断点处续传足彩期数获得相关场次ID，i=list.index(value)


from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup as bs
import time
import csv
import re

gamelink = []

url = "http://zx.500.com/zc/lsdz.php"


def getgamelink(lid):
    src = driver.page_source
    soup = bs(src, "lxml")
    for link in soup.find_all("a", string="亚"):
        try:
            glink = link.get("href")
            p = re.compile(r"\d{6}")
            gamelink.append((lid, p.search(glink).group(), glink))
        except BaseException:
            print("broke at page reading")
            return False
    return True


driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true'])
driver.get(url)
elem = driver.find_element_by_tag_name("select")
elemselect = Select(elem)
lotteryidlist = elem.text.split()
lotteryidlistlen = len(lotteryidlist)
i = lotteryidlist.index("14036")  # 根据断点内容找位置
print("this is the start: ", lotteryidlist[i])
while i < lotteryidlistlen:
    try:
        if (getgamelink(lotteryidlist[i])):
            i += 1
            lotteryid = lotteryidlist[i]
            print(lotteryid)
            elemselect.select_by_value(lotteryid)
            time.sleep(4)
            elem = driver.find_element_by_tag_name("select")
            elemselect = Select(elem)
        else:
            print("broke at page reading if sentence")
            break
    except BaseException:
        print("broke at new dynamic content")
        break

print("this is the end: ", lotteryid)

with open("alink_continue4.csv", "w") as f:
    f_csv = csv.writer(f)
    f_csv.writerows(gamelink)

print("done")
