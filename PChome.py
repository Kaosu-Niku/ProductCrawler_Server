import time
import requests
import sys
sys.stdout.reconfigure(encoding='utf-8')
# code 參考 https://blog.jiatool.com/posts/pchome_spider01/ 

class PchomeSpider():
    """PChome線上購物 爬蟲"""

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0',
        }

    def request_get(self, url, params=None, to_json=True):
        # XHR 裡面有個請求包含搜尋結果，prods 裡面有每項商品
        """送出 GET 請求

        :param url: 請求網址
        :param params: 傳遞參數資料
        :param to_json: 是否要轉為 JSON 格式
        :return data: requests 回應資料
        """
        r = requests.get(url, params)
        if r.status_code != requests.codes.ok:
            print(f'網頁載入發生問題：{url}')
        try:
            if to_json:
                # 將結果轉為 json 格式
                data = r.json()
            else:
                data = r.text
            # print(data)
        except Exception as e:
            print(e)
            return None
        return data

    def search_products(self, keyword, max_page=100, shop='全部', sort='有貨優先', price_min=-1, price_max=-1, is_store_pickup=False, is_ipost_pickup=False):
        """搜尋商品

        :param keyword: 搜尋關鍵字
        :param max_page: 抓取最大頁數，預設 100 頁
        :param shop: 賣場類別 (全部、24h購物、24h書店、廠商出貨、PChome旅遊)
        :param sort: 商品排序 (有貨優先、精準度、價錢由高至低、價錢由低至高、新上市)
        :param price_min: 篩選"最低價" (需與 price_max 同時用)
        :param price_max: 篩選"最高價" (需與 price_min 同時用)
        :param is_store_pickup: 篩選"超商取貨"
        :param is_ipost_pickup: 篩選"i 郵箱取貨"
        :return products: 搜尋結果商品
        """
         # 各式篩選條件
        all_shop = {
            '全部': 'all',
            '24h購物': '24h',
            '24h書店': '24b',
            '廠商出貨': 'vdr',
            'PChome旅遊': 'tour',
        }
        all_sort = {
            '有貨優先': 'sale/dc',
            '精準度': 'rnk/dc',
            '價錢由高至低': 'prc/dc',
            '價錢由低至高': 'prc/ac',
            '新上市': 'new/dc',
        }

        # 篩選條件對應 url 後方帶的參數，關鍵字放在 q 參數內
        url = f'https://ecshweb.pchome.com.tw/search/v3.3/{all_shop[shop]}/results'
        
        params = {
            'q': keyword,  # 關鍵字
            'sort': all_sort[sort],  # 排序依據
            'page': 0   # 頁數
        }
        products = []

        if price_min >= 0 and price_max >= 0:
            params['price'] = f'{price_min}-{price_max}'   # 篩選價格範圍
        if is_store_pickup:
            params['cvs'] = 'all'   # 超商取貨
        if is_ipost_pickup:
            params['ipost'] = 'Y'   # i 郵箱取貨

        while params['page'] < max_page:
            params['page'] += 1
            time.sleep(0.1)
            data = self.request_get(url, params)
            if not data:
                print(f'請求發生錯誤：{url}{params}')
                break
            if data['totalRows'] <= 0:
                print('找不到有關的產品')
                break
            if data['totalPage'] <= params['page']:
                # 若總頁面數 <= 搜尋頁面 (預設100頁)，則搜尋結束
                break
            products.extend(data['prods'])
        return products
    
    # 只爬1頁產品
    def search_products1(self, keyword, shop='全部'):
        # 各式篩選條件
        all_shop = {
            '全部': 'all',
            '24h購物': '24h',
            '24h書店': '24b',
            '廠商出貨': 'vdr',
            'PChome旅遊': 'tour',
        }

        # 篩選條件對應 url 後方帶的參數，關鍵字放在 q 參數內
        url = f'https://ecshweb.pchome.com.tw/search/v3.3/{all_shop[shop]}/results'
        
        params = {
            'q': keyword,  # 關鍵字
            'page': 1   # 頁數
        }
        products = []

        time.sleep(0.1)
        data = self.request_get(url, params)
        if not data:
            print(f'請求發生錯誤：{url}{params}')
        if data['totalRows'] <= 0:
            print('找不到有關的產品')
        products.extend(data['prods'])
           
        return products