# 此段代码用于根据足彩期数获得相关场次ID，
# 涉及知识点：
# 1.使用selenium 控制基于javascript的动态网页
# 2.使用beautifulsoup 获取页面内容
# 3.列表，正则表达示字符串处理
# 4.CSV文档写入（一次性）
# 5.异常处理


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
i = 0
print("this is the start: ", lotteryidlist[i])
while i < lotteryidlistlen:
    try:
        if (getgamelink(lotteryidlist[i])):
            i += 1
            lotteryid = lotteryidlist[i]
            print(lotteryid)
            elemselect.select_by_value(lotteryid)
            time.sleep(3)
            elem = driver.find_element_by_tag_name("select")
            elemselect = Select(elem)
        else:
            print("broke at page reading if sentence")
            break
    except BaseException:
        print("broke at new dynamic content")
        break

print("this is the end: ", lotteryid)

with open("alink.csv", "w") as f:
    f_csv = csv.writer(f)
    f_csv.writerows(gamelink)

print("done")



