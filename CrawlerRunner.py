import json
import momo as Momo
import PChome  as PChome
import yahoo as Yahoo
import os

class Product:
    def __init__(self, shop, name, price, link, image):
        self.shop = shop
        self.name = name
        self.price = price
        self.link = link
        self.image = image
class Runner:

    def momoCrawler(self, keyword):
        momo = Momo.MomoSpider()
        products = momo.search_products1(keyword)
        productList = list()
        for x in range(len(products)):
            newProduct = { "ProductShop":'momo',"ProductName":products[x][0],"ProductPrice":products[x][1],"ProductLink":products[x][2],"ProductImage":products[x][3]}
            productList.append(newProduct)
        jsonData = {"Product":productList}
        return json.dumps(jsonData) 

    def pchomeCrawler(self, keyword):
        pchome = PChome.PchomeSpider()
        products = pchome.search_products1(keyword)
        productList = list()
        for x in range(len(products)):
            newProduct = { "ProductShop":'PChome',"ProductName":products[x]['name'],"ProductPrice":products[x]['price'],"ProductLink":'https://24h.pchome.com.tw/prod/' + products[x]['Id'],"ProductImage":'https://cs-a.ecimg.tw' + products[x]['picB']}
            productList.append(newProduct)
        jsonData = {"Product":productList}
        return json.dumps(jsonData) 

    def yahooCrawler(self, keyword):
        yahoo = Yahoo.yahooSpider()
        products = yahoo.search_products1(keyword)
        productList = list()
        for x in range(len(products)):
            newProduct = { "ProductShop":'Yahoo',"ProductName":products[x][0],"ProductPrice":products[x][1],"ProductLink": products[x][2],"ProductImage":products[x][3]}
            productList.append(newProduct)
        jsonData = {"Product":productList}
        return json.dumps(jsonData) 

    # #todo 將商品資訊轉換成json資料格式
    # def outputJsonType(self,productList):
    #     #todo 將執行路徑切換至該檔案的資料夾路徑(絕對路徑)，以將後續的JSON檔生成在該路徑下
    #     # __file__ 取得當前執行檔案的相對路徑(相對於python解釋器的路徑)
    #     # os.path.dirname() 將檔案路徑轉為資料夾路徑 ex: C:/folder/data.txt => C:/folder/
    #     # os.path.abspath() 將相對路徑轉為絕對路徑
    #     dataPath = os.path.abspath(os.path.dirname(__file__))
    #     os.chdir(dataPath)
    #     #todo 創建一個Json檔並寫入資訊
    #     productFile = open('ProductData.json','w',encoding='UTF-8')
    #     productFile.writelines('{\n')
    #     productFile.writelines('\"Product\":[\n')
    #     for x in productList["Product"]:  
    #         try:
    #             productFile.writelines('{\n')    
    #             productFile.writelines(f'\"ProductShop\":\"{x["ProductShop"]}\",\n') #商品網站  
    #             productFile.writelines(f'\"ProductName\":\"{x["ProductName"]}\",\n') #商品名稱
    #             productFile.writelines(f'\"ProductPrice\":\"{x["ProductPrice"]}\",\n') #商品價格
    #             productFile.writelines(f'\"ProductLink\":\"{x["ProductLink"]}\",\n') #商品連結
    #             productFile.writelines(f'\"ProductImage\":\"{x["ProductImage"]}\"\n') #商品圖片
    #             if productList["Product"].index(x) != productList["Product"].index(productList["Product"][-1]):
    #                 productFile.writelines('},\n')
    #             else:
    #                 productFile.writelines('}\n')
    #         except:
    #             print(f'商品寫入錯誤')
    #     productFile.writelines(']\n')
    #     productFile.writelines('}')
    #     productFile.close() 