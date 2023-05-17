import requests
from bs4 import BeautifulSoup
import time
import sys
sys.stdout.reconfigure(encoding='utf-8')

class MomoSpider():
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0',
        }

    def search_products(self, keyword):
        pages = 30
        products =[]
        for page in range(1, pages):
            url = 'https://m.momoshop.com.tw/search.momo?searchKeyword={}&cpCode=&couponSeq=&searchType=1&cateLevel=-1&curPage={}&cateCode=&cateName=&maxPage=26&minPage=1&_advCp=N&_advFirst=N&_advFreeze=N&_advSuperstore=N&_advTvShop=N&_advTomorrow=N&_advNAM=N&_advStock=N&_advPrefere=N&_advThreeHours=N&_advVideo=N&_advCycle=N&_advCod=N&_advSuperstorePay=N&_advPriceS=&_advPriceE=&_brandNameList=&_brandNoList=&brandSeriesStr=&isBrandSeriesPage=0&ent=b&_imgSH=fourCardType&specialGoodsType=&_isFuzzy=0&_spAttL=&_mAttL=&_sAttL=&_noAttL=&topMAttL=&topSAttL=&topNoAttL=&hotKeyType=0&hashTagCode=&hashTagName='.format(keyword, page)
            # print(url)
            time.sleep(0.1)
            resp = requests.get(url, headers=self.headers)

            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, "html.parser")
                for item in soup.select('li.goodsItemLi.goodsItemLiSeo'):
                    name = item.select('div.prdInfoWrap > div.prdNameTitle')[0].text
                    name = name[1:-1] # 去除名稱頭尾的 \n

                    # 當搜尋頁數超過最大頁數時，網頁會呈現最後一頁的內容
                    # 因此當爬到重複的商品名稱時，結束爬蟲
                    if name not in products:
                        url = item.select('a')[0].get('href')
                        link = 'https://m.momoshop.com.tw'+url
                        price = item.select('div.prdInfoWrap > p.priceArea > span.priceSymbol > b.price')[0].text
                        pic = item.select('a > div.prdImgWrap.swiperArea.swiper-container.manyPics > div.swiper-wrapper > div.swiper-slide > img')[0].get('src')
                        pro = [name, price, link, pic]
                        products.append(pro)
                    else:
                        break
        return products
    
    def search_products1(self, keyword):
        pages = 2
        products =[]
        for page in range(1, pages):
            url = 'https://m.momoshop.com.tw/search.momo?searchKeyword={}&cpCode=&couponSeq=&searchType=1&cateLevel=-1&curPage={}&cateCode=&cateName=&maxPage=26&minPage=1&_advCp=N&_advFirst=N&_advFreeze=N&_advSuperstore=N&_advTvShop=N&_advTomorrow=N&_advNAM=N&_advStock=N&_advPrefere=N&_advThreeHours=N&_advVideo=N&_advCycle=N&_advCod=N&_advSuperstorePay=N&_advPriceS=&_advPriceE=&_brandNameList=&_brandNoList=&brandSeriesStr=&isBrandSeriesPage=0&ent=b&_imgSH=fourCardType&specialGoodsType=&_isFuzzy=0&_spAttL=&_mAttL=&_sAttL=&_noAttL=&topMAttL=&topSAttL=&topNoAttL=&hotKeyType=0&hashTagCode=&hashTagName='.format(keyword, page)
            resp = requests.get(url, headers=self.headers)

            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, "html.parser")
                for item in soup.select('li.goodsItemLi.goodsItemLiSeo'):
                    name = item.select('div.prdInfoWrap > div.prdNameTitle')[0].text
                    name = name[1:-1] # 去除名稱頭尾的 \n
                    name = name.replace('"', ' ')
                    name = name.replace('\\', ' ')
                    if name in products:
                        break
                    else:
                        url = item.select('a')[0].get('href')
                        link = 'https://m.momoshop.com.tw'+url
                        price = item.select('div.prdInfoWrap > p.priceArea > span.priceSymbol > b.price')[0].text
                        pic = item.select('a > div.prdImgWrap.swiperArea.swiper-container.manyPics > div.swiper-wrapper > div.swiper-slide > img')[0].get('src')
                        pro = [name, price, link, pic]
                        products.append(pro)
        return products
