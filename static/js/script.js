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
