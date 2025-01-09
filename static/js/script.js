// Tạo sự kiện hover lâu hơn 2 giây để hiển thị popup
let currentImage = document.getElementById("current-image");
let detailPopup = document.getElementById("detail-popup");
let hoverTimer;

// Khi chuột vào ảnh
currentImage.addEventListener("mouseenter", function() {
  hoverTimer = setTimeout(function() {
    // Hiển thị popup dưới ảnh hiện tại
    detailPopup.style.display = "block";
    detailPopup.style.opacity = 1;
  }, 500); // 2 giây
});

// Khi chuột ra khỏi ảnh
currentImage.addEventListener("mouseleave", function() {
  clearTimeout(hoverTimer); // Hủy bỏ nếu chuột rời trước 2 giây
  detailPopup.style.display = "none";
  detailPopup.style.opacity = 0; // Ẩn popup
});

let currentImageFiles = [];  // Biến lưu danh sách ảnh hiện tại

// Hàm khởi tạo để gọi API lần đầu tiên
function init() {
    fetch('/imagesList')  // Thay đổi URL API nếu cần
        .then(response => response.json())  // Chuyển dữ liệu từ JSON
        .then(data => {
            let imageFiles = data.map(item => item.filename);  // Giả sử API trả về các đối tượng có thuộc tính "filename"

            // Giới hạn số lượng ảnh hiển thị tối đa là 10 ảnh
            if (imageFiles.length > 10) {
                imageFiles = imageFiles.slice(0, 10);
            }

            // Cập nhật lại danh sách ảnh hiện tại
            currentImageFiles = imageFiles;

            // Chọn tất cả các thẻ <img> trong div với id "initial-images" và "more-images"
            const initialImages = document.querySelectorAll('#initial-images .history-image');
            const moreImages = document.querySelectorAll('#more-images .history-image');

            // Cập nhật các ảnh trong "initial-images" (3 ảnh đầu tiên)
            for (let i = 0; i < 3; i++) {
                if (currentImageFiles[i]) {
                    // Cập nhật src và alt cho ảnh
                    initialImages[i].src = '/static/resources/result/' + currentImageFiles[i];
                    initialImages[i].alt = 'Updated History Image ' + (i + 1);

                    // Đảm bảo xóa display: none nếu có
                    initialImages[i].style.removeProperty('display');
                } else {
                    // Ẩn các ảnh nếu không có trong danh sách
                    initialImages[i].style.display = 'none';
                }
            }

            // Cập nhật các ảnh trong "more-images" (7 ảnh còn lại)
            for (let i = 0; i < 7; i++) {
                if (currentImageFiles[i + 3]) {  // Bắt đầu từ ảnh thứ 4 (index 3)
                    // Cập nhật src và alt cho ảnh
                    moreImages[i].src = '/static/resources/result/' + currentImageFiles[i + 3];
                    moreImages[i].alt = 'Updated History Image ' + (i + 4);

                    // Đảm bảo xóa display: none nếu có
                    moreImages[i].style.removeProperty('display');
                } else {
                    // Ẩn các ảnh nếu không có trong danh sách
                    moreImages[i].style.display = 'none';
                }
            }

        })
        .catch(error => {
            // Xử lý lỗi nếu có
            console.error('Lỗi khi gọi API: ', error);
        });
}

// Gọi init() lần đầu tiên khi trang web được tải
init();

// Lặp lại mỗi 5 giây để cập nhật danh sách ảnh
setInterval(function() {
    fetch('/imagesList')  // Thay đổi URL API nếu cần
        .then(response => response.json())  // Chuyển dữ liệu từ JSON
        .then(data => {
            let imageFiles = data.map(item => item.filename);  // Giả sử API trả về các đối tượng có thuộc tính "filename"

            // Giới hạn số lượng ảnh hiển thị tối đa là 10 ảnh
            if (imageFiles.length > 10) {
                imageFiles = imageFiles.slice(0, 10);
            }

            // Kiểm tra nếu danh sách ảnh mới khác với danh sách hiện tại
            if (JSON.stringify(imageFiles) !== JSON.stringify(currentImageFiles)) {
                // Cập nhật lại danh sách ảnh hiện tại
                currentImageFiles = imageFiles;

                // Chọn tất cả các thẻ <img> trong div với id "initial-images" và "more-images"
                const initialImages = document.querySelectorAll('#initial-images .history-image');
                const moreImages = document.querySelectorAll('#more-images .history-image');

                // Cập nhật các ảnh trong "initial-images" (3 ảnh đầu tiên)
                for (let i = 0; i < 3; i++) {
                    if (currentImageFiles[i]) {
                        // Cập nhật src và alt cho ảnh
                        initialImages[i].src = '/static/resources/result/' + currentImageFiles[i];
                        initialImages[i].alt = 'Updated History Image ' + (i + 1);

                        // Đảm bảo xóa display: none nếu có
                        initialImages[i].style.removeProperty('display');
                    } else {
                        // Ẩn các ảnh nếu không có trong danh sách
                        initialImages[i].style.display = 'none';
                    }
                }

                // Cập nhật các ảnh trong "more-images" (7 ảnh còn lại)
                for (let i = 0; i < 7; i++) {
                    if (currentImageFiles[i + 3]) {  // Bắt đầu từ ảnh thứ 4 (index 3)
                        // Cập nhật src và alt cho ảnh
                        moreImages[i].src = '/static/resources/result/' + currentImageFiles[i + 3];
                        moreImages[i].alt = 'Updated History Image ' + (i + 4);

                        // Đảm bảo xóa display: none nếu có
                        moreImages[i].style.removeProperty('display');
                    } else {
                        // Ẩn các ảnh nếu không có trong danh sách
                        moreImages[i].style.display = 'none';
                    }
                }
            }
        })
        .catch(error => {
            // Xử lý lỗi nếu có
            console.error('Lỗi khi gọi API: ', error);
        });
}, 5000);  // Lặp lại mỗi 5 giây

document.addEventListener("DOMContentLoaded", function() {
  // Lấy tất cả các ảnh trong phần lịch sử
  const historyImages = document.querySelectorAll('.history-image');

  // Lấy phần ảnh hiện tại
  const currentImage = document.getElementById('current-image');
  
  // Lấy phần chi tiết ảnh
  const detailTimestamp = document.getElementById('detail-timestamp');
  const detailSize = document.getElementById('detail-size');  // Giả sử bạn có phần hiển thị kích thước ảnh
  const detailFormat = document.getElementById('detail-format'); // Giả sử bạn có phần hiển thị định dạng ảnh

  // Lắng nghe sự kiện click trên các ảnh lịch sử
  historyImages.forEach(image => {
      image.addEventListener('click', function() {
          // Khi một ảnh lịch sử được click, cập nhật ảnh hiện tại
          const clickedImageSrc = image.src;  // Lấy src của ảnh đã click
          
          // Cập nhật ảnh hiện tại
          currentImage.src = clickedImageSrc;
          currentImage.alt = image.alt;

          // Lấy thông tin chi tiết từ API
          fetch('/imagesList')  // Gọi API lấy thông tin ảnh (đảm bảo đúng URL)
            .then(response => response.json())  // Chuyển dữ liệu từ JSON
            .then(data => {
                // Tìm ảnh đã được chọn trong mảng data
                const selectedImage = data.find(img => 
                    '/static/resources/result/' + img.fileName === clickedImageSrc
                );

                if (selectedImage) {
                    // Cập nhật thông tin chi tiết cho ảnh đã chọn
                    detailTimestamp.textContent = selectedImage.fileTime;
                    detailSize.textContent = selectedImage.fileSize;
                    detailFormat.textContent = selectedImage.fileFormat;
                }
            })
            .catch(error => {
                console.error('Lỗi khi gọi API: ', error);
            });
      });
  });
});

