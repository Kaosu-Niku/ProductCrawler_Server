from flask import Flask, jsonify, send_from_directory, render_template ,url_for
from flask_cors import CORS
import CrawlerRunner as CR

app = Flask(__name__, static_url_path='/',static_folder='./static')

CORS(app)

@app.route('/')
def index():
    return 'hello world'
    # return send_from_directory('static', 'index.html')

@app.route('/search/momo/keyword=<keyword>')

def get_momo_data(keyword):
    crawlerRunner = CR.Runner()
    momoData = crawlerRunner.momoCrawler(keyword)
    return momoData

@app.route('/search/pchome/keyword=<keyword>')

def get_pchome_data(keyword):
    crawlerRunner = CR.Runner()
    pchomeData = crawlerRunner.pchomeCrawler(keyword)
    return pchomeData

@app.route('/search/yahoo/keyword=<keyword>')

def get_yahoo_data(keyword):
    crawlerRunner = CR.Runner()
    yahooData = crawlerRunner.yahooCrawler(keyword)
    return yahooData

# # 設置靜態文件路徑
# @app.route('/static/<path:path>')
# def send_static(path):
#     return send_from_directory('static', path)