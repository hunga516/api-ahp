import os
import pandas as pd
from pymongo import MongoClient
from bson.decimal128 import Decimal128
from bson import ObjectId  # Import ObjectId

# Kết nối MongoDB
client = MongoClient("mongodb+srv://opolo4847:moips103@cluster0.ikaskks.mongodb.net/")
db = client["coffeeDB"]
collection = db["Test"]

df = pd.read_excel("AHP_Coffee_Data.xlsx")

data = df.to_dict(orient="records") 

def convert_doc(doc):
    doc["_id"] = ObjectId()
    
    if "chi_phi_thue" in doc:
        doc["chi_phi_thue"] = Decimal128(str(doc["chi_phi_thue"]))
    if "muc_thu_nhap_tb" in doc:
        doc["muc_thu_nhap_tb"] = Decimal128(str(doc["muc_thu_nhap_tb"]))
    if "dien_tich_tb" in doc:
        doc["dien_tich_tb"] = float(doc["dien_tich_tb"])
    if "imageURL" in doc:
        filename = str(doc["imageURL"]).strip()
        doc["imageURL"] = os.path.join("images", filename)   
    return doc

data_converted = [convert_doc(doc) for doc in data]

result = collection.insert_many(data_converted)
print("Import thành công!")
