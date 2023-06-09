from flask import Flask, jsonify, send_from_directory, render_template ,url_for
import CrawlerRunner as CR
from flask_cors import CORS

app = Flask(__name__, static_url_path='/',static_folder='./static')

CORS(app)

@app.route('/')
def index():
    return 'hello world'

@app.route('/search/momo/keyword=<keyword>')

def get_momo_data(keyword):
    crawlerRunner = CR.Runner()
    momoData = crawlerRunner.momoCrawler(keyword)
    res = app.make_response(momoData)
    res.headers['Content-Type'] = 'application/json'
    return res

@app.route('/search/pchome/keyword=<keyword>')

def get_pchome_data(keyword):
    crawlerRunner = CR.Runner()
    pchomeData = crawlerRunner.pchomeCrawler(keyword)
    res = app.make_response(pchomeData)
    res.headers['Content-Type'] = 'application/json'
    return res

@app.route('/search/yahoo/keyword=<keyword>')

def get_yahoo_data(keyword):
    crawlerRunner = CR.Runner()
    yahooData = crawlerRunner.yahooCrawler(keyword)
    res = app.make_response(yahooData)
    res.headers['Content-Type'] = 'application/json'
    return res

# # 設置靜態文件路徑
# @app.route('/static/<path:path>')
# def send_static(path):
#     return send_from_directory('static', path)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=3000,debug=True)
