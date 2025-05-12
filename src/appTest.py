from flask import Flask, request, jsonify, send_from_directory, render_template
from pymongo import MongoClient
from bson.decimal128 import Decimal128
from flask_cors import CORS
import os

app = Flask(__name__, template_folder=".")
CORS(app)

client = MongoClient("mongodb+srv://opolo4847:moips103@cluster0.ikaskks.mongodb.net/")
db = client["coffeeDB"]
collection = db["Test"]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/data', methods=['GET'])
def get_data():
    query = {}
    
    # Lấy tham số khu_vuc
    khu_vuc = request.args.get('khu_vuc')
    if khu_vuc and khu_vuc.strip() != "":
        query['khu_vuc'] = khu_vuc.strip()
    
    # Lấy tham số chi_phi_thue
    chi_phi_thue = request.args.get('chi_phi_thue')
    if chi_phi_thue and chi_phi_thue.strip() != "":
        try:
            query['chi_phi_thue'] = float(chi_phi_thue)
        except ValueError:
            return jsonify({"error": "Giá trị chi_phi_thue không hợp lệ"}), 400

    # Lấy tham số muc_thu_nhap_tb
    muc_thu_nhap_tb = request.args.get('muc_thu_nhap_tb')
    if muc_thu_nhap_tb and muc_thu_nhap_tb.strip() != "":
        try:
            query['muc_thu_nhap_tb'] = float(muc_thu_nhap_tb)
        except ValueError:
            return jsonify({"error": "Giá trị muc_thu_nhap_tb không hợp lệ"}), 400

    # Lấy tham số dien_tich_tb
    dien_tich_tb = request.args.get('dien_tich_tb')
    if dien_tich_tb and dien_tich_tb.strip() != "":
        try:
            query['dien_tich_tb'] = float(dien_tich_tb)
        except ValueError:
            return jsonify({"error": "Giá trị dien_tich_tb không hợp lệ"}), 400


    docs_cursor = collection.find(query)
    results = []
    for doc in docs_cursor:
        doc["_id"] = str(doc["_id"])
        for key, value in doc.items():
            if isinstance(value, Decimal128):
                doc[key] = float(value.to_decimal())

        # if "imageURL" in doc:
        #     doc["imageURL"] = os.path.basename(doc["imageURL"])
        # results.append(doc)
        
        if "imageURL" in doc:
            doc["imageURL"] = doc["imageURL"].replace("\\", "/")
            doc["imageURL"] = os.path.basename(doc["imageURL"])
        results.append(doc)
    
    if not results:
        return jsonify({"error": "Không tìm thấy document nào"}), 404

    return jsonify(results)

@app.route('/images/<path:filename>')
def serve_image(filename):
    image_folder = os.path.join(os.path.dirname(__file__), 'images')
    return send_from_directory(image_folder, filename)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
