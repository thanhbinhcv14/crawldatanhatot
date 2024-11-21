import pandas as pd
from sqlalchemy import create_engine, text
import numpy as np

# Đọc dữ liệu từ file CSV
file_path = 'nhatot/spiders/nhatotdata.csv'  # Thay đổi đường dẫn đến file CSV của bạn
data = pd.read_csv(file_path)

# Hàm chuyển đổi giá trị thành số
def convert_to_numeric(value, unit_multiplier):
    try:
        value = value.strip()  # Loại bỏ khoảng trắng dư thừa
        value = value.replace(',', '.')  # Đổi dấu phẩy thành dấu chấm cho số thập phân
        return float(value) * unit_multiplier
    except ValueError:
        return None

def convert_price(value):
    value = value.strip()  # Loại bỏ khoảng trắng dư thừa
    if ' tỷ' in value:
        return convert_to_numeric(value.replace(' tỷ', ''), 1e9)
    elif ' triệu' in value:
        return convert_to_numeric(value.replace(' triệu', ''), 1e6)
    else:
        return None  # Nếu không có đơn vị

def convert_price_m2(value):
    value = value.strip()  # Loại bỏ khoảng trắng dư thừa
    if ' triệu/m²' in value:
        return convert_to_numeric(value.replace(' triệu/m²', ''), 1e6)
    elif ' tỷ/m²' in value:
        return convert_to_numeric(value.replace(' tỷ/m²', ''), 1e9)
    else:
        return None  # Nếu không có đơn vị

# Áp dụng hàm vào các cột
data['price'] = data['price'].apply(convert_price)
data['price_m2'] = data['price_m2'].apply(convert_price_m2)

# Xử lý cột 'land_area_m2'
data['land_area_m2'] = data['land_area_m2'].replace({' m²': '', ',': '', 'Không có diện tích': np.nan}, regex=True)
data['land_area_m2'] = pd.to_numeric(data['land_area_m2'], errors='coerce')

# Xử lý các giá trị NaN
data.dropna(subset=['price', 'price_m2', 'land_area_m2'], inplace=True)

# Thay thế các chuỗi không cần thiết và chuyển đổi thành NaN nếu không có thông tin
data['rooms'] = data['rooms'].replace({' phòng': '', 'Không có thông tin số phòng': np.nan}, regex=True)

# Chuyển đổi thành kiểu số
data['rooms'] = pd.to_numeric(data['rooms'], errors='coerce')

# Tách dữ liệu thành bảng Properties
properties_columns = [
    'name', 'price', 'address', 'price_m2', 'rooms', 'house_type',
    'legal_document', 'land_area_m2'
]
properties = data[properties_columns].copy()
properties['Property_ID'] = range(1, len(properties) + 1)  # Tạo ID cho mỗi bất động sản
properties = properties[['Property_ID'] + properties_columns]  # Đặt lại thứ tự cột

# Tách dữ liệu thành bảng Property Characteristics
characteristics_columns = ['descriptions']
characteristics = data[['name'] + characteristics_columns].copy()
characteristics['Characteristic_ID'] = range(1, len(characteristics) + 1)  # Tạo ID cho mỗi đặc điểm
characteristics = characteristics.rename(columns={'name': 'Property_Name'})

# Tạo bảng cho House Types
house_types = properties[['house_type']].drop_duplicates().reset_index(drop=True)
house_types['HouseType_ID'] = range(1, len(house_types) + 1)
house_types = house_types[['HouseType_ID', 'house_type']]

# Tạo bảng cho Legal Documents
legal_documents = properties[['legal_document']].drop_duplicates().reset_index(drop=True)
legal_documents['LegalDocument_ID'] = range(1, len(legal_documents) + 1)
legal_documents = legal_documents[['LegalDocument_ID', 'legal_document']]

# Thêm HouseType_ID và LegalDocument_ID vào bảng Properties
properties = properties.merge(house_types, on='house_type', how='left')
properties = properties.merge(legal_documents, on='legal_document', how='left')

# Thêm Property_ID vào bảng characteristics dựa trên vị trí
characteristics['Property_ID'] = properties['Property_ID'].values[:len(characteristics)]

# Kết nối đến cơ sở dữ liệu PostgreSQL mặc định
postgres_user = 'thanhbinh'          
postgres_password = 'thanhbinh1'  
postgres_host = 'localhost'       
postgres_port = '5432'             
postgres_db = 'nhatot_daxuly'  # Đặt tên cho cơ sở dữ liệu bạn muốn tạo

# Tạo URL kết nối đến PostgreSQL
db_url = f'postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}'
engine = create_engine(db_url)

# Hàm để tạo database và cấp quyền
def create_database_and_grant_privileges(db_name):
    with engine.connect() as connection:
        # Tạo database nếu chưa tồn tại
        connection.execute(text(f"SELECT 'CREATE DATABASE {db_name}' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '{db_name}');"))
        connection.execute(text(f"COMMIT;"))  # Đảm bảo rằng lệnh trên đã được thực thi

        # Cấp quyền cho người dùng trên schema public
        connection.execute(text(f"GRANT ALL PRIVILEGES ON SCHEMA public TO {postgres_user};"))

# Gọi hàm tạo database và cấp quyền
create_database_and_grant_privileges(postgres_db)

# Kết nối đến database đã tạo
engine = create_engine(f'postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}')

# Lưu các bảng vào PostgreSQL
properties.to_sql('properties', engine, if_exists='replace', index=False)
characteristics.to_sql('property_characteristics', engine, if_exists='replace', index=False)
house_types.to_sql('house_types', engine, if_exists='replace', index=False)
legal_documents.to_sql('legal_documents', engine, if_exists='replace', index=False)

print("Đã hoàn thành xử lý dữ liệu và lưu vào PostgreSQL!") 


#-----------------------------------------------------------------------------------------------

from pymongo import MongoClient

# Kết nối tới MongoDB mặc định
mongo_host = 'localhost'
mongo_port = '27017'
mongo_db_name = 'nhatot_mongodb'

# Tạo URL kết nối đến MongoDB (mặc định không có xác thực)
client = MongoClient(f'mongodb://{mongo_host}:{mongo_port}/')

# Chọn cơ sở dữ liệu MongoDB
mongo_db = client[mongo_db_name]

# Hàm lưu DataFrame vào MongoDB
def save_to_mongodb(df, collection_name):
    collection = mongo_db[collection_name]
    # Xóa dữ liệu cũ trong collection trước khi thêm mới
    collection.delete_many({})
    # Chuyển đổi DataFrame thành danh sách từ điển và chèn vào collection
    collection.insert_many(df.to_dict('records'))

# Lưu các bảng vào MongoDB
save_to_mongodb(properties, 'properties')
save_to_mongodb(characteristics, 'property_characteristics')
save_to_mongodb(house_types, 'house_types')
save_to_mongodb(legal_documents, 'legal_documents')

print("Đã hoàn thành xử lý dữ liệu và lưu vào MongoDB!")
