from flask import Flask, request, jsonify
from scraper_scholar import get_scholar_data
from scraper_garuda import get_publications

app = Flask(__name__)

@app.route('/scrape_scholar', methods=['GET'])
def scrape_scholar():
    scholar_id = request.args.get('scholar_id')
    if not scholar_id:
        return jsonify({"error": "scholar_id parameter is required"}), 400

    data = get_scholar_data(scholar_id)
    return jsonify(data)

@app.route('/scrape_garuda', methods=['GET'])
def scrape_garuda():
    garuda_id = request.args.get('garuda_id')
    if not garuda_id:
        return jsonify({"error": "garuda_id parameter is required"}), 400

    data = get_publications(garuda_id)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)