import time
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

''' 
    未解决问题：
    1、小说章节分多页显示，只能获取第一页。
    2‘使用多线程爬取不能保证顺序。
    （不使用多线程挺慢的）
'''

root_url = "https://www.biqudi.cc/bi/3723/"
#打开浏览器（指定浏览器）
driver = webdriver.Chrome()

#打开网站
driver.get(root_url)
# 等待按钮变得可点击，然后点击它
#wait = WebDriverWait(driver, 5)  # 等待最多15秒
cla = driver.find_elements(by=By.CLASS_NAME,value="box_con")

element = driver.find_element(by=By.XPATH, value='//*[@id="list"]/dl[4]/dt/span')
#点击全部目录按钮
element.click()

#获取章节链接
aLinks = driver.find_elements(by=By.XPATH, value='//*[@id="newlist"]/dd/a')

ahref = []
for link in aLinks:
    href =link.get_attribute("href")
    #print(href)
    if href:
        ahref.append(href)

print(ahref)
#print(response.status_code)

# 关闭浏览器
driver.quit()

#获取小说章节内容文本
atext =[]
def get_ZJ_content(url):

    response =requests.get(url)
    if response.status_code !=200:
        raise Exception("响应错误")
    soup = BeautifulSoup(response.content, "html.parser", from_encoding="utf-8")

    title = soup.find("h1", class_="bookname").get_text()
    content = soup.find("div", id="booktxt").find_all('p')
    content = f"{title}{content}"

    atext.append(content)

count = 1
import threading

#创建线程
threads = []
for url in ahref:
    #设置线程
    thread = threading.Thread(target=get_ZJ_content,args=(url,))
    threads.append(thread)
    #准备
    thread.start()
    #get_ZJ_content(url)


#等待所有线程完成
for thread in threads:
    print("进行到：{},总：{}".format(count, len(ahref)))
    thread.join()
    count += 1

stext=" ".join(atext)
with open("小说-剑来.txt", 'w',encoding='utf-8') as f:
    f.write(stext)