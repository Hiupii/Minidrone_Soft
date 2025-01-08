from ultralytics import YOLO
import cv2
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

# Load the YOLO model
model_path = "best.pt"  # Update with the path to your model
model = YOLO(model_path)

# Set the input image directory and output directory
input_dir = "../static/resources/uploads"  # Replace with the path to your input images directory
output_dir = "../static/resources/result"  # Path to save annotated images

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Class name mapping
class_name_mapping = {0: "Circle", 1: "Rectangle", 2: "Triangle"}

# Function to process and annotate images
def process_image(file_path):
    # Wait for the file to stabilize
    max_retries = 5
    for attempt in range(max_retries):
        try:
            initial_size = os.path.getsize(file_path)
            time.sleep(0.1)  # Wait 100ms
            current_size = os.path.getsize(file_path)
            if initial_size == current_size:
                break
        except Exception as e:
            print(f"Error checking file size: {e}")
            return

    # Read the image after the check
    image = cv2.imread(file_path)
    if image is None:
        print(f"Error: Unable to read image {file_path} after {max_retries} retries. Skipping...")
        return

    # Generate output file name
    base_name = os.path.basename(file_path)
    name, ext = os.path.splitext(base_name)
    output_file = f"{name}_result{ext}"
    output_path = os.path.join(output_dir, output_file)

    # Predict and process the image
    results = model.predict(source=image, conf=0.5, save=False, stream=True)

    # Annotate results on the image
    for result in results:
        boxes = result.boxes.xyxy.cpu().numpy()
        confidences = result.boxes.conf.cpu().numpy()
        class_ids = result.boxes.cls.cpu().numpy().astype(int)

        for box, confidence, class_id in zip(boxes, confidences, class_ids):
            xmin, ymin, xmax, ymax = map(int, box)
            class_name = class_name_mapping.get(class_id, str(class_id))  # Map class_id to name
            label = f"{class_name} {confidence:.2f}"  # Display block name and confidence
            cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
            cv2.putText(image, label, (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Save the annotated image
    cv2.imwrite(output_path, image)
    print(f"Annotated image saved at {output_path}")

# Watchdog event handler
class NewImageHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            print(f"New image detected: {event.src_path}")
            process_image(event.src_path)

# Set up Watchdog observer
event_handler = NewImageHandler()
observer = Observer()
observer.schedule(event_handler, path=input_dir, recursive=False)

# Start the observer
observer.start()
print(f"Monitoring directory: {input_dir}")

try:
    while True:
        time.sleep(1)  # Keep the main thread alive
except KeyboardInterrupt:
    print("Stopping directory monitoring...")
    observer.stop()

observer.join()
