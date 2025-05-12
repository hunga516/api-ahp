from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS
from pymongo import MongoClient
from bson.decimal128 import Decimal128
from datetime import datetime
import os

app = Flask(__name__, template_folder=".")
CORS(app)

# Kết nối MongoDB
client = MongoClient("mongodb+srv://opolo4847:moips103@cluster0.ikaskks.mongodb.net/")
db = client["coffeeDB"]
collection = db["Test"]
projects_collection = db["project"]  # Collection cho project

# Trang chủ
@app.route('/')
def index():
    return render_template('index.html')

# API lấy dữ liệu từ collection Test
@app.route('/data', methods=['GET'])
def get_data():
    query = {}

    khu_vuc = request.args.get('khu_vuc')
    if khu_vuc and khu_vuc.strip() != "":
        query['khu_vuc'] = khu_vuc.strip()

    chi_phi_thue = request.args.get('chi_phi_thue')
    if chi_phi_thue and chi_phi_thue.strip() != "":
        try:
            query['chi_phi_thue'] = float(chi_phi_thue)
        except ValueError:
            return jsonify({"error": "Giá trị chi_phi_thue không hợp lệ"}), 400

    muc_thu_nhap_tb = request.args.get('muc_thu_nhap_tb')
    if muc_thu_nhap_tb and muc_thu_nhap_tb.strip() != "":
        try:
            query['muc_thu_nhap_tb'] = float(muc_thu_nhap_tb)
        except ValueError:
            return jsonify({"error": "Giá trị muc_thu_nhap_tb không hợp lệ"}), 400

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

        if "imageURL" in doc:
            doc["imageURL"] = doc["imageURL"].replace("\\", "/")
            doc["imageURL"] = os.path.basename(doc["imageURL"])

        results.append(doc)

    if not results:
        return jsonify({"error": "Không tìm thấy document nào"}), 404

    return jsonify(results)

# API phục vụ ảnh
@app.route('/images/<path:filename>')
def serve_image(filename):
    image_folder = os.path.join(os.path.dirname(__file__), 'images')
    return send_from_directory(image_folder, filename)

# API kiểm tra
@app.route('/api', methods=['GET'])
def hello():
    return jsonify({"message": "hi"})

# API tạo project mới
@app.route('/api/projects', methods=['POST'])
def save_project():
    try:
        data = request.json
        project_id = data.get('id', str(datetime.now().timestamp()))

        if 'timestamp' not in data:
            data['timestamp'] = datetime.now().isoformat()

        result = projects_collection.insert_one({
            '_id': project_id,
            **data
        })

        return jsonify({
            'success': True,
            'message': 'Dự án đã được lưu thành công',
            'project_id': str(result.inserted_id)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

# API lấy tất cả project
@app.route('/api/projects', methods=['GET'])
def get_projects():
    try:
        projects = list(projects_collection.find({}))
        for project in projects:
            project['id'] = str(project.pop('_id'))

        return jsonify({
            'success': True,
            'projects': projects
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

# API lấy project theo ID
@app.route('/api/projects/<project_id>', methods=['GET'])
def get_project(project_id):
    try:
        project = projects_collection.find_one({'_id': project_id})

        if not project:
            return jsonify({
                'success': False,
                'message': 'Dự án không tồn tại'
            }), 404

        project['id'] = str(project.pop('_id'))

        return jsonify({
            'success': True,
            'project': project
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

# Chạy app
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
