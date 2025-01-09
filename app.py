from flask import Flask, send_from_directory, Response
from flask import render_template, url_for, make_response, request, session, redirect, flash, jsonify
from util import *
from werkzeug.serving import WSGIRequestHandler
import time

WSGIRequestHandler.protocol_version = "HTTP/1.1"

# Init app
app = Flask(__name__)
app.secret_key = 'MiniDrone'
# Đặt biến flag để theo dõi thay đổi
fileChangeFlag = False

# Main page
@app.route('/')
def index():
    cookie = request.cookies.get('username')
    if cookie is not None:
        imagesList = get_image_files()
        return render_template('index.html', images = imagesList)
    else:
        return redirect(url_for('login_page'))

# Login page
@app.route('/login')
def login_page():
    return render_template('login.html')

# # API trả về danh sách 10 ảnh mới nhất (tên file)
@app.route('/imagesList')
def api_images():
    imagesData = get_image_files()
    images = []
    for data in imagesData:
        images.append(data["fileName"])
    # Trả về danh sách các từ điển với khóa 'filename'
    return jsonify([{"filename": image} for image in images])

@app.route('/imagesDetail')
def api_images_detail():
    imagesData = get_image_files()
    return imagesData

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
    global fileChangeFlag
    try:
        if request.headers.get('Content-Type') == 'image/jpeg':
            image_data = request.get_data()

            if not image_data:
                return "No image data received", 400

            # Tạo tên file dựa trên thời gian
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            file_name = f"uploaded_image_{timestamp}.jpg"
            file_path = os.path.join("./static/resources/uploads", file_name)

            # Đảm bảo thư mục lưu ảnh tồn tại
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # Lưu ảnh
            with open(file_path, 'wb') as f:
                f.write(image_data)

            fileChangeFlag = True

            return f"Image uploaded successfully as {file_name}!", 200
        else:
            return "Invalid Content-Type", 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


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

