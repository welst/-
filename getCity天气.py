import pandas
import requests
import lxml
url = "https://tianqi.2345.com/Pc/GetHistory"
#header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"}

#为了处理只有User-Agent和参数会报403错误。抖音学的
headers ={'Accept':'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding':'gzip, deflate, br, zstd',
            'Accept-Language':'zh-CN,zh;q=0.9',
            'Connection':'keep-alive',
            'Cookie':'Hm_lvt_a3f2879f6b3620a363bec646b7a8bcdd=1713505015; Hm_lpvt_a3f2879f6b3620a363bec646b7a8bcdd=1713511809; lastCountyId=70141; lastCountyTime=1713511809; lastCountyPinyin=libo; lastProvinceId=17; lastCityId=57827',
            'Host':'tianqi.2345.com',
            'Referer':'https://tianqi.2345.com/wea_history/70141.htm',
            #Sec-Ch-Ua: Chromium;v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"
            #Sec-Ch-Ua-Mobile:?0
            #Sec-Ch-Ua-Platform:"Windows"
            #Sec-Fetch-Dest:empty
            #Sec-Fetch-Mode:cors
            #Sec-Fetch-Site:same-origin
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
           #'X-Requested-With':'XMLHttpRequest'
            }

def DataWith(data_json):
    data = data_json.json()["data"]
    print(data)
    df = pandas.read_html(data)[0]
    return df


datas =[]
for year in range(2023,2024):
    for month in range(1,13):
        #省份，城市代码，年，月
        aparam = {"areaInfo[areaId]":70141, "areaInfo[areaType]":2, "date[year]":year, "date[month]":month}

        response = requests.get(url,headers=headers,params=aparam)
        print(url)
        print(aparam)
        print(response.status_code)
        if(response.status_code !=200):
            raise Exception("请求响应错误！")
        data_json = response.json()["data"]
        print("data_json",data_json)
        df = pandas.read_html(data_json)[0]
        print("df",df)
        datas.append(df)
        #print("datas",datas)


pandas.concat(datas).to_excel("天气.xlsx",index =False)