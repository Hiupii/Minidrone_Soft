from flask import Flask, jsonify, send_from_directory
import os
from flask import render_template, url_for, make_response, request, session, redirect, flash, jsonify
from util import *

# Init app
app = Flask(__name__)
app.secret_key = 'MiniDrone'

# Main page
@app.route('/')
def index():
    cookie = request.cookies.get('username')
    if cookie is not None:
        return render_template('index.html')
    else:
        return redirect(url_for('login_page'))

# Login page
@app.route('/login')
def login_page():
    return render_template('login.html')

# API list
@app.route('/login', methods=['POST', 'GET'])
def Login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        login_status = VerifyLogin(username, password)

        if login_status == True:
            index = make_response(redirect(url_for('index')))
            index.set_cookie('username', username, max_age=360)
            # index.set_cookie('ncode_username', utility.encode(username, "hoankiem"))
            return index
        else:
            flash('Invalid username or password', 'error')

    return render_template('login.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    try:
        # Kiểm tra nếu dữ liệu được gửi dưới dạng binary
        if 'Content-Type' in request.headers and request.headers['Content-Type'] == 'image/jpeg':
            # Lấy dữ liệu ảnh từ body của request
            image_data = request.get_data()

            # Tạo đường dẫn file để lưu ảnh
            file_path = os.path.join("uploads", "uploaded_image.jpg")

            # Ghi dữ liệu ảnh ra file
            with open(file_path, 'wb') as f:
                f.write(image_data)

            return "Image uploaded successfully!", 200
        else:
            return "Invalid Content-Type", 400
    except Exception as e:
        return f"Error: {str(e)}", 500

# Định nghĩa đường dẫn tới thư mục chứa ảnh
IMAGE_FOLDER = os.path.join(os.getcwd(), 'static/resources')

# @app.route('/get-images', methods=['GET'])
# def get_images():
#     try:
#         # Lấy tất cả các tệp trong thư mục resources
#         files = os.listdir(IMAGE_FOLDER)
        
#         # Lọc chỉ những tệp ảnh (jpg, jpeg, png, gif)
#         images = [file for file in files if file.lower().endswith(('jpg', 'jpeg', 'png', 'gif'))]
        
#         # Trả về danh sách ảnh dưới dạng JSON
#         return jsonify(images)
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# # Cung cấp các tệp tĩnh như hình ảnh từ thư mục 'static/resources'
# @app.route('/static/resources/<filename>')
# def send_image(filename):
#     return send_from_directory(IMAGE_FOLDER, filename)

app.run(debug=True, host = "0.0.0.0", port=5000)

