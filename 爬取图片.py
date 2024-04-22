import requests
from bs4 import BeautifulSoup
import os
import threading

def download_image(image_url, save_dir, file_name):
    # 确保保存目录存在
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

        # 拼接完整的文件保存路径
    save_path = os.path.join(save_dir, file_name)

    # 发送HTTP请求获取图片
    response = requests.get(image_url, stream=True)

    # 检查请求是否成功
    if response.status_code == 200:
        # 打开文件以二进制写入模式
        with open(save_path, 'wb') as file:
            # 遍历响应内容的数据块并将其写入文件
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"Image downloaded and saved to {save_path}")
    else:
        print(f"Failed to download image from {image_url}, status code: {response.status_code}")


alist = []
def DwithHtml(NodeUrl):
    header = {
        "User-Agent": """Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"""}

    response = requests.get(NodeUrl, headers=header)

    print(response.encoding)
    if response.status_code != 200:
        raise Exception("响应错误！")



    soup = BeautifulSoup(response.content, "html.parser", from_encoding="utf-8")
    #print(soup)

    alink = soup.find("div", class_="slist").find_all("img")

    for link in alink:

        href = link.get("src")
        name = link.get("alt")
        aZuhe =(href,name)
        if href:
            href = "https://pic.netbian.com"+href
            alist.append(aZuhe)

    #print("单页的图片地址",alist)


#线程方法
def threedFiction(Fic,aUrl,save_dir=None, file_name=None):
    threads =[]
    #配置线程
    for url in aUrl:
        if not save_dir:
            threed = threading.Thread(target=Fic, args=(url,))
        else:
            threed = threading.Thread(target=Fic, args=(url, save_dir, file_name,))

        threads.append(threed)
        threed.start()

    #等待所有线程完成
    count = 1
    for thread in threads:
        print("进行到：{},总：{}".format(count, len(aUrl)))
        thread.join()
        count += 1

def threedFiction2(Fic,aUrl):
    threads =[]
    #配置线程
    for item in aUrl:
        image_url = "https://pic.netbian.com"+item[0]  # 替换为实际的图片URL
        save_dir = "./path/4k图片/"
        file_name = item[1] + ".jpg"  # 自定义的图片名称

        threed = threading.Thread(target=Fic, args=(image_url, save_dir, file_name,))
        threads.append(threed)
        threed.start()

    #等待所有线程完成
    count = 1
    for thread in threads:
        print("进行到：{},总：{}".format(count, len(aUrl)))
        thread.join()
        count += 1

#第1到第22页地址
aRootUrl =[]
for i in range(1,23):
    if i<2:
        url = "https://pic.netbian.com/4kdongwu/"
    else:
        url = "https://pic.netbian.com/4kdongwu/index_{}.html".format(i)
    aRootUrl.append(url)
print(aRootUrl)

threedFiction(DwithHtml,aRootUrl)

print("总的图片地址：",alist)

# 下载图片

image_url = "https://pic.netbian.com/uploads/allimg/170317/174750-1489744070b09c.jpg"  # 替换为实际的图片URL
save_dir = "./path/4K图片"  # 替换为实际的保存目录
file_name = "一只跃起的猎豹图片.jpg"  # 自定义的图片名称

#download_image(image_url, save_dir, file_name)
#多线程下载
threedFiction2(download_image,alist)


