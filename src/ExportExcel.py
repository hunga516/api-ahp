import pandas as pd
from pymongo import MongoClient
from bson.decimal128 import Decimal128

client = MongoClient("mongodb+srv://opolo4847:moips103@cluster0.ikaskks.mongodb.net/")
db = client["coffeeDB"]
collection = db["Khu_Vuc"]

cursor = collection.find({})
data = list(cursor)
 
for doc in data:
    doc["_id"] = str(doc["_id"])
    if "chi_phi_thue" in doc and isinstance(doc["chi_phi_thue"], Decimal128):
        doc["chi_phi_thue"] = float(doc["chi_phi_thue"].to_decimal())
    if "muc_thu_nhap_tb" in doc and isinstance(doc["muc_thu_nhap_tb"], Decimal128):
        doc["muc_thu_nhap_tb"] = float(doc["muc_thu_nhap_tb"].to_decimal())

df = pd.DataFrame(data)

df.to_excel("AHP_Coffee_Data.xlsx", index=False)
print("Thành công!")
