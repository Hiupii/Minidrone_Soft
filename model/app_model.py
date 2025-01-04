import torch

model_path = "/home/hieu/Documents/PlatformIO/Projects/datn/software/model/best.pt"

model = YourModelClass()
model.load_state_dict(torch.load(model_path))

print("Load ok")

model.eval()

from torchvision import transforms

# Chuyển đổi dữ liệu đầu vào (ví dụ: hình ảnh) thành tensor
transform = transforms.Compose([
    transforms.Resize((224, 224)),  # Resize hình ảnh nếu cần
    transforms.ToTensor(),          # Chuyển đổi sang Tensor
])

# Ví dụ: xử lý hình ảnh đầu vào
from PIL import Image
image = Image.open("./image.png")
input_tensor = transform(image).unsqueeze(0)  # Thêm batch dimension

# Chuyển input_tensor sang thiết bị phù hợp (CPU hoặc GPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
input_tensor = input_tensor.to(device)

# Thực hiện suy luận
output = model(input_tensor)

# Chuyển đổi kết quả nếu cần
predicted_class = torch.argmax(output, dim=1)
print(f"Predicted Class: {predicted_class.item()}")