import requests
from bs4 import BeautifulSoup
import time
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

class yahooSpider():
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0',
        }

    def requests_get(self, url, params=None):
        res = requests.get(url, params, headers = self.headers)

        # 指定編碼為 utf-8，並忽略無法轉換的字符
        content = res.content.decode('utf-8', 'ignore')
        soup = BeautifulSoup(content, 'html.parser')

        # 請求結果的 json 檔藏在 html 的這個 div 的 'data-state' 裡面
        div = soup.find_all('div', {'id':'isoredux-data'})[0]['data-state']
        my_json = json.loads(div)

        r = requests.get(my_json["search"]["utherUrl"]) # json 檔的 url
        data = r.json()["result"]["ecsearch"]["hits"] # 產品資訊

        return data

    def search_products(self, keyword, max_page=20):
        url = 'https://tw.bid.yahoo.com/search/auction/product'
        params = {
            'p': keyword,  # 關鍵字
            'pg': 0  # 頁碼
        }
        products = []
        # print('yahoo啟動')
        # 當頁碼小於最大頁碼 (預設20頁) 時，進入迴圈
        while params['pg'] < max_page:
            params['pg'] += 1
            time.sleep(0.1)

            data = self.requests_get(url, params)
            if not data:
                print(f'請求發生錯誤：{url}{params}')
                break
            if len(data) <= 0:
                print('找不到有關的產品')
                break
            for i in range(len(data)):
                name = data[i]["ec_title"]
                price = data[i]["ec_price"]
                link = data[i]["ec_item_url"]
                pic = data[i]["ec_image"]

                pro = [name, price, link, pic]
                products.append(pro)
            
        return products
    
    # 只爬1頁產品
    def search_products1(self, keyword):
        url = 'https://tw.bid.yahoo.com/search/auction/product'
        params = {
            'p': keyword,  # 關鍵字
            'pg': 1  # 頁碼
        }
        products = []

        time.sleep(0.1)
        data = self.requests_get(url, params)
        if not data:
            print(f'請求發生錯誤：{url}{params}')
        if len(data) <= 0:
            print('找不到有關的產品')

        for i in range(len(data)):
            name = data[i]["ec_title"]
            name = name.replace('"', '')
            name = name.replace('\\', '')
            name = name.replace('～', '')
            name = name.replace('，', '')
            name = name.replace('×', '')
            name = name.replace(' ', '')
            price = data[i]["ec_price"]
            link = data[i]["ec_item_url"]
            pic = data[i]["ec_image"]

            pro = [name, price, link, pic]
            products.append(pro)
        # print(products)
        return products




