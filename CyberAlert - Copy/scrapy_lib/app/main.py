# app/main.py
from flask import Flask, request, jsonify
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

app = Flask(__name__)

# Initialize Scrapy crawler process
process = CrawlerProcess(get_project_settings())

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.json
    spider_name = data.get('cyware') # rapid7, cert , threatpost

    if not spider_name:
        return jsonify({"error": "spider_name is required"}), 400

    # Start the Scrapy spider
    process.crawl(spider_name)
    process.start()

    return jsonify({"message": f"{spider_name} spider started"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
