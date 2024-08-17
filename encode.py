import os
import cv2
import numpy as np
import tkinter as tk
from tkinter import messagebox
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Function to preprocess images (resize, normalize, and histogram equalization)
def preprocess_image(image, size=(100, 100)):
    image = cv2.resize(image, size)
    image = cv2.equalizeHist(image)
    return image

# Function to load images and labels for training
def load_images_and_labels(data_dir):
    image_paths = []
    labels = []

    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if file.endswith(".jpg"):
                image_path = os.path.join(root, file)
                label = os.path.basename(root)  # Label is the directory name (student roll number)
                image_paths.append(image_path)
                labels.append(int(label))  # Convert roll number to integer for LBPH model

    images = []
    for image_path in image_paths:
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        image = preprocess_image(image)
        images.append(image)

    return images, np.array(labels)

# Function to augment data
def augment_data(images, labels):
    augmented_images = []
    augmented_labels = []

    for image, label in zip(images, labels):
        augmented_images.append(image)
        augmented_labels.append(label)

        # Data augmentation
        augmented_images.append(cv2.flip(image, 1))  # Horizontal flip
        augmented_labels.append(label)

        # Add more augmentations if needed
        rows, cols = image.shape

        # Rotation
        M = cv2.getRotationMatrix2D((cols/2, rows/2), 15, 1)
        rotated_image = cv2.warpAffine(image, M, (cols, rows))
        augmented_images.append(rotated_image)
        augmented_labels.append(label)

        # Translation
        M = np.float32([[1, 0, 5], [0, 1, 5]])
        translated_image = cv2.warpAffine(image, M, (cols, rows))
        augmented_images.append(translated_image)
        augmented_labels.append(label)

    return augmented_images, augmented_labels

# Function to train LBPH model
def train_lbph_model(data_dir, info_label):
    info_label.set("Encoding faces...")

    images, labels = load_images_and_labels(data_dir)
    images, labels = augment_data(images, labels)

    # Initialize LBPH face recognizer
    recognizer = cv2.face.LBPHFaceRecognizer_create(radius=1, neighbors=8, grid_x=8, grid_y=8)

    # Train the recognizer with loaded faces and IDs
    recognizer.train(images, np.array(labels))

    # Save the trained model
    model_file = "lbph_model.yml"
    recognizer.save(model_file)
    print(f"LBPH model trained and saved as {model_file}")
    info_label.set("Encoding complete")

    # Evaluate the model
    y_pred = []
    for image in images:
        label, confidence = recognizer.predict(image)
        y_pred.append(label)

    accuracy = accuracy_score(labels, y_pred)
    print(f"Model accuracy: {accuracy * 100:.2f}%")

    return recognizer

# Main function to handle encoding process
def encode_faces_main(data_directory):
    root = tk.Tk()
    root.withdraw()  # Hide the main tkinter window

    # Train or load the LBPH model
    info_label = tk.StringVar()
    train_lbph_model(data_directory, info_label)

if __name__ == "__main__":
    data_directory = "C:/Users/Vaidehi Suryawanshi/Downloads/Student Attendance (1)/Student Attendance/data/student"
    encode_faces_main(data_directory)
