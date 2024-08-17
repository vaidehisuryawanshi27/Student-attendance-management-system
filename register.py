import tkinter as tk
from tkinter import messagebox
import cv2
import os
import shutil
import pandas as pd
from PIL import Image, ImageTk

# Function to capture images with face detection and save them
def capture_images(student_name, student_id, num_images=50, img_format='jpg'):
    directory = f"C:/Users/Vaidehi Suryawanshi/Downloads/Student Attendance (1)/Student Attendance/data/student/{student_id}"
    if not os.path.exists(directory):
        os.makedirs(directory)
    else:
        response = messagebox.askyesno("Student Exists", f"Student with Roll Number {student_id} already registered. Overwrite previous data?")
        if response:
            shutil.rmtree(directory)
            os.makedirs(directory)
            # Remove existing entry in Excel sheet
            remove_existing_student(student_id)
        else:
            messagebox.showinfo("Data Kept", f"Keeping previous data for Roll Number {student_id}")
            return

    # Show warning message
    messagebox.showwarning("Warning", "Remove all accessories that might cover your face and make sure your face is clearly visible")

    haarcasecade_path = "C:/Users/Vaidehi Suryawanshi/Downloads/Student Attendance (1)/Student Attendance/haarcascade_frontalface_default.xml"
    face_cascade = cv2.CascadeClassifier(haarcasecade_path)

    cap = cv2.VideoCapture(0)
    count = 0

    while count < num_images:
        ret, frame = cap.read()
        if not ret:
            continue

        # Convert frame to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            # Draw a rectangle around the detected face
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

            # Save the detected face region (grayscale)
            img_name = f"{directory}/{student_name}_{student_id}_{count+1}.{img_format}"
            cv2.imwrite(img_name, gray[y:y+h, x:x+w])

            count += 1

        cv2.imshow("Capture Images", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

    # Show a pop-up message with the number of captured images
    messagebox.showinfo("Image Capture", f"Captured {count} images for {student_name} ({student_id})")

    # Save student details to Excel sheet
    save_to_excel(student_name, student_id)

    # Close the registration window
    register_window.destroy()

# Function to remove existing student data from the Excel sheet
def remove_existing_student(student_id):
    excel_file = "C:/Users/Vaidehi Suryawanshi/Downloads/Student Attendance (1)/Student Attendance/data/registrations/students.xlsx"
    
    if os.path.exists(excel_file):
        df = pd.read_excel(excel_file)
        df = df[df["Roll Number"] != int(student_id)]
        df.to_excel(excel_file, index=False)

# Function to save student details to an Excel sheet
def save_to_excel(student_name, student_id):
    excel_file = "C:/Users/Vaidehi Suryawanshi/Downloads/Student Attendance (1)/Student Attendance/data/registrations/students.xlsx"
    
    if os.path.exists(excel_file):
        df = pd.read_excel(excel_file)
    else:
        df = pd.DataFrame(columns=["Name", "Roll Number"])

    # Check if the roll number already exists
    if student_id in df["Roll Number"].values:
        messagebox.showerror("Input Error", f"Roll Number {student_id} already exists.")
        return

    new_row = pd.DataFrame({"Name": [student_name], "Roll Number": [student_id]})
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_excel(excel_file, index=False)

# Function to handle registration process
def register_student_window():
    global register_window

    register_window = tk.Tk()
    register_window.title("Register Student")

    # Set the size of the window
    register_window.geometry('600x400')

    # Load background image and resize it to fit the window
    img = Image.open("C:/Users/Vaidehi Suryawanshi/Downloads/Student Attendance (1)/Student Attendance/1.jpg")
    img = img.resize((600, 400))  # Resize the image to fit the window size
    background_image = ImageTk.PhotoImage(img)

    background_label = tk.Label(register_window, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Create a frame to hold the widgets
    frame = tk.Frame(register_window, bg='#ffeae6')  # Set frame background color
    frame.pack(expand=True)

    tk.Label(frame, text="Student Name", font=("Arial", 14), bg='#ffeae6', fg='black').pack(padx=10, pady=10)  # Set label colors
    name_entry = tk.Entry(frame, font=("Arial", 14))
    name_entry.pack(padx=10, pady=5)

    tk.Label(frame, text="Roll Number", font=("Arial", 14), bg='#ffeae6', fg='black').pack(padx=10, pady=10)  # Set label colors
    roll_number_entry = tk.Entry(frame, font=("Arial", 14))
    roll_number_entry.pack(padx=10, pady=5)

    def register_student():
        student_name = name_entry.get()
        student_id = roll_number_entry.get()

        if not student_name or not student_id:
            messagebox.showerror("Input Error", "Please enter both name and roll number")
            return

        if not student_id.isdigit():
            messagebox.showerror("Input Error", "Roll number should contain only digits")
            return

        capture_images(student_name, student_id)

    register_button = tk.Button(frame, text="Register", command=register_student, font=("Arial", 14), bg='#ffb6c1')  # Set button background color
    register_button.pack(padx=10, pady=20)

    register_window.mainloop()

if __name__ == "__main__":
    register_student_window()
