from flask import Flask
from routes.scraper import scraper_bp
from routes.analyzer import analyzer_bp

app = Flask(__name__)

# 註冊路由 (分流)
app.register_blueprint(scraper_bp, url_prefix='/api/scraper')
app.register_blueprint(analyzer_bp, url_prefix='/api/analyzer')

@app.route('/health', methods=['GET'])
def health():
    return "Sidecar is running"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
