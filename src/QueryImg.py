from flask import Flask, request, jsonify, send_from_directory, render_template
from pymongo import MongoClient
from bson.decimal128 import Decimal128
import os

app = Flask(__name__, template_folder=".")

client = MongoClient("mongodb+srv://opolo4847:moips103@cluster0.ikaskks.mongodb.net/")
db = client["coffeeDB"]
collection = db["Test"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data', methods=['GET'])
def get_data_by_khu_vuc():
    khu_vuc = request.args.get('khu_vuc')
    if not khu_vuc:
        return jsonify({"error": "Thiếu tên khu vực"}), 400

    data = collection.find_one({"khu_vuc": khu_vuc})
    if not data:
        return jsonify({"error": "Không tìm thấy khu vực"}), 404


    data["_id"] = str(data["_id"])
    for key, value in data.items():
        if isinstance(value, Decimal128):
            data[key] = float(value.to_decimal())

    if "imageURL" in data:
        data["imageURL"] = os.path.basename(data["imageURL"])

    return jsonify(data)

@app.route('/images/<path:filename>')
def serve_image(filename):
    image_folder = os.path.join(os.path.dirname(__file__), 'images')
    return send_from_directory(image_folder, filename)

if __name__ == '__main__':
    app.run(debug=True)
