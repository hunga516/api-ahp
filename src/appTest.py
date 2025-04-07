from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.decimal128 import Decimal128

app = Flask(__name__)

client = MongoClient("mongodb+srv://opolo4847:moips103@cluster0.ikaskks.mongodb.net/")
db = client["coffeeDB"]
collection = db["Khu_Vuc"]

@app.route('/data', methods=['GET'])
def get_data():
    query = {}

    price_param = request.args.get('price')
    if price_param:
        try: 
            price = float(price_param)
            query["chi_phi_thue"] = price
        except ValueError:
            return jsonify({"error": "Thất bại"}), 400

    invoice_param = request.args.get('invoice')
    if invoice_param:
        try:
            invoice = float(invoice_param)
            query["muc_thu_nhap_tb"] = invoice
        except ValueError:
            return jsonify({"error": "Thất bại"}), 400

    area_param = request.args.get('area')
    if area_param:
        try:
            area = float(area_param)
            query["dien_tich_tb"] = area
        except ValueError:
            return jsonify({"error": "Thất bại"}), 400

    data_cursor = collection.find(query)
    data = []
    for doc in data_cursor:
        doc["_id"] = str(doc["_id"])
        for key, value in doc.items():
            if isinstance(value, Decimal128):
                doc[key] = float(value.to_decimal())
        data.append(doc)

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
