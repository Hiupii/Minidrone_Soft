from ultralytics import YOLO
import cv2
import os

# Load the YOLO model
model_path = "best.pt"  # Update with the path to your model
model = YOLO(model_path)

# Set the input image directory and output directory
input_dir = "./"  # Replace with the path to your input images directory
output_dir = "./result"  # Path to save annotated images

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Class name mapping
name = {'0': 'Circle', '1': 'Rectangle', '2': 'Triangle'}

# Process each image in the input directory
for filename in os.listdir(input_dir):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):  # Check for image files
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)

        # Read the image
        image = cv2.imread(input_path)
        if image is None:
            print(f"Error: Unable to read image {input_path}. Skipping...")
            continue

        # Perform object detection on the image
        results = model.predict(source=image, conf=0.5, save=False, stream=True)

        # Annotate the image with detection results
        for result in results:
            boxes = result.boxes.xyxy.cpu().numpy()  # Get bounding box coordinates
            confidences = result.boxes.conf.cpu().numpy()  # Get confidence scores
            class_ids = result.boxes.cls.cpu().numpy().astype(int)  # Get class IDs

            for box, confidence, class_id in zip(boxes, confidences, class_ids):
                # Unpack box coordinates
                xmin, ymin, xmax, ymax = map(int, box)
                label = f"{name[model.names[class_id]]} {confidence:.2f}"  # Get class name and confidence

                # Draw the bounding box and label on the image
                cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
                cv2.putText(image, label, (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Save the annotated image
        cv2.imwrite(output_path, image)
        print(f"Annotated image saved at {output_path}")

print("Processing completed.")
