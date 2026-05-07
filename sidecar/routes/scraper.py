from flask import Blueprint, jsonify, request
import requests
from bs4 import BeautifulSoup

scraper_bp = Blueprint('scraper', __name__)

@scraper_bp.route('/scrape', methods=['GET'])
def scrape():
    target_url = request.args.get('url')
    if not target_url:
        return jsonify({"error": "Missing url parameter"}), 400
    
    try:
        response = requests.get(target_url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string if soup.title else "No title found"
        return jsonify({"status": "success", "url": target_url, "title": title.strip()})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
