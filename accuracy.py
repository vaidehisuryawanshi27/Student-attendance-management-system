import cv2
import os
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix

# Function to load images and labels from a directory
def load_images_from_folder(folder):
    images = []
    labels = []
    label_map = {}
    for subdir in os.listdir(folder):
        subdir_path = os.path.join(folder, subdir)
        if os.path.isdir(subdir_path):
            roll_number = int(subdir)  # Assuming subdirectory names are roll numbers
            label_map[roll_number] = subdir
            for filename in os.listdir(subdir_path):
                img_path = os.path.join(subdir_path, filename)
                img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                if img is not None:
                    images.append(img)
                    labels.append(roll_number)
    return images, labels, label_map

# Path to the test dataset
test_data_path = 'C:/Users/Vaidehi Suryawanshi/Downloads/Student Attendance (1)/Student Attendance/data/test'

# Load test images and their corresponding labels
test_images, test_labels, label_map = load_images_from_folder(test_data_path)

# Load the trained LBPH model
model = cv2.face.LBPHFaceRecognizer_create()
model.read('lbph_model.yml')

# Predict the labels for the test images
predicted_labels = []
for img in test_images:
    label, confidence = model.predict(img)
    predicted_labels.append(label)

# Calculate accuracy
accuracy = np.sum(np.array(predicted_labels) == np.array(test_labels)) / len(test_labels)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

# Generate confusion matrix
unique_labels = sorted(set(test_labels) | set(predicted_labels))
conf_matrix = confusion_matrix(test_labels, predicted_labels, labels=unique_labels)

# Create a DataFrame for the confusion matrix with proper labels
label_names = [label_map.get(i, f"Unknown-{i}") for i in unique_labels]
conf_matrix_df = pd.DataFrame(conf_matrix, index=label_names, columns=label_names)

# Print confusion matrix
print("\nConfusion Matrix:")
print(conf_matrix_df)
