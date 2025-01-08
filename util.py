import json, os
from pathlib import Path
from datetime import datetime

def VerifyLogin(username, password):
    with open('./static/resources/logindata.json', 'r') as file:
        droneData = json.load(file)
        
    for data in droneData:
        if data["username"].lower() == username.lower() and data["password"] == password:
            return True
    return False

# Thư mục chứa ảnh
folderPath = Path('static/resources/result')

def extract_time_from_filename(filename):
    # Tên file có định dạng "uploaded_image_YYYYMMDD_HHMMSS_result.jpg"
    # Lấy phần thời gian trong tên file: YYYYMMDD_HHMMSS
    timestamp_str = filename.split('_')[2] + "_" + filename.split('_')[3]
    return datetime.strptime(timestamp_str, '%Y%m%d_%H%M%S')

# print(extract_time_from_filename("uploaded_image_20250108_215240_result.jpg"))

# Lấy danh sách ảnh từ thư mục (chỉ lấy tên file và sắp xếp theo thời gian sửa đổi)
def get_image_files():
    files = [f.name for f in folderPath.iterdir() if f.is_file()]

    # Sắp xếp các file theo thời gian, mới nhất trước
    sorted_files = sorted(files, key=extract_time_from_filename, reverse=True)

    return sorted_files[:10]

# print(get_image_files())