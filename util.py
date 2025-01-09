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

def format_date(date_str):
    # Chuyển đổi định dạng YYYYMMDD thành YYYY-MM-DD
    year = date_str[:4]
    month = date_str[4:6]
    day = date_str[6:8]
    return f"{year}-{month}-{day}"

def format_time(time_str):
    # Chuyển đổi định dạng HHMMSS thành HH:MM:SS
    hours = time_str[:2]
    minutes = time_str[2:4]
    seconds = time_str[4:6]
    return f"{hours}:{minutes}:{seconds}"

# Lấy danh sách ảnh từ thư mục (chỉ lấy tên file và sắp xếp theo thời gian sửa đổi)
def get_image_files():
    files = [f.name for f in folderPath.iterdir() if f.is_file()]
    returnData = []
    # Sắp xếp các file theo thời gian, mới nhất trước
    sorted_files = sorted(files, key=extract_time_from_filename, reverse=True)
    for file in sorted_files:
        fileName = file
        fileTime = str(format_date(file.split("_")[2])) + " " + str(format_time(file.split("_")[3]))
        fileSize = "300x150"
        fileFormat = "JPEG"
        fileDetail = {
            "fileName": fileName,
            "fileTime": fileTime,
            "fileSize": fileSize,
            "fileFormat": fileFormat,
        }
        returnData.append(fileDetail)
    return returnData[:10]

print(get_image_files())