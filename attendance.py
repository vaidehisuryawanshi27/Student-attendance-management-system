import cv2
import os
import pandas as pd
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, Radiobutton
from PIL import Image, ImageTk

# List of subjects
subjects = ['AI', 'DMBI', 'EH', 'WT']

# Function to get student details by roll number
def get_student_details(roll_number):
    excel_file = "C:/Users/Vaidehi Suryawanshi/Downloads/Student Attendance (1)/Student Attendance/data/registrations/students.xlsx"
    if os.path.exists(excel_file):
        df = pd.read_excel(excel_file)
        student = df[df['Roll Number'] == int(roll_number)]
        if not student.empty:
            return student.iloc[0]['Name']
    return None

# Function to log attendance
def log_attendance(subject):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('C:/Users/Vaidehi Suryawanshi/Downloads/Student Attendance (1)/Student Attendance/lbph_model.yml')

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    cap = cv2.VideoCapture(0)
    start_time = datetime.now()

    roll_number = None

    while (datetime.now() - start_time).seconds < 10:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            face = gray[y:y+h, x:x+w]
            roll_number, confidence = recognizer.predict(face)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.putText(frame, f"Roll No: {roll_number}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    if roll_number is not None:
        student_name = get_student_details(roll_number)
        if student_name:
            response = messagebox.askyesno("Log Attendance", f"Log attendance for {student_name} Roll No: {roll_number}?")
            if response:
                date_str = datetime.now().strftime('%Y-%m-%d')
                attendance_dir = f'C:/Users/Vaidehi Suryawanshi/Downloads/Student Attendance (1)/Student Attendance/data/attendance/{subject}'
                os.makedirs(attendance_dir, exist_ok=True)
                file_path = os.path.join(attendance_dir, f'{date_str}.xlsx')

                if os.path.exists(file_path):
                    df = pd.read_excel(file_path)
                else:
                    df = pd.DataFrame(columns=['Name', 'Roll Number', 'Timestamp'])

                # Check if the roll number already exists for today's attendance
                if roll_number in df['Roll Number'].values:
                    messagebox.showwarning("Warning", f"Attendance for Roll No: {roll_number} already logged.")
                    return False

                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                new_entry = pd.DataFrame({'Name': [student_name], 'Roll Number': [roll_number], 'Timestamp': [timestamp]})
                df = pd.concat([df, new_entry], ignore_index=True)
                df = df[['Name', 'Roll Number', 'Timestamp']]
                df.to_excel(file_path, index=False)  # Save to Excel file

                # Show success message after saving Excel file
                messagebox.showinfo("Success", "Attendance logged successfully.")
                return True
            else:
                # Ask user to retry if attendance is not logged
                messagebox.showinfo("Retry", "Please retry marking attendance.")
                return False
        else:
            messagebox.showerror("Error", "Student not found in registration records.")
            return False
    return False

# Main function to create the attendance logging UI
def main():
    root = tk.Tk()
    root.title("Mark Attendance")
    root.geometry('600x400')

    # Load background image and resize it to fit the window
    img = Image.open("C:/Users/Vaidehi Suryawanshi/Downloads/Student Attendance (1)/Student Attendance/1.jpg")
    img = img.resize((600, 400))
    background_image = ImageTk.PhotoImage(img)

    # Create a frame with a background image
    frame = tk.Frame(root)
    frame.place(relwidth=1, relheight=1)

    # Display background image using a label
    background_label = tk.Label(frame, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Create a sub-frame to hold the subject-related widgets
    subject_frame = tk.Frame(frame, bg='#ffeae6')
    subject_frame.pack(expand=True, pady=50)

    # Label for subjects
    tk.Label(subject_frame, text="Select Subject", font=("Arial", 14), bg='#ffeae6', fg='black').pack()

    selected_subject = tk.StringVar()
    selected_subject.set(None)  # Set initially no option selected

    def on_subject_select():
        subject_value = selected_subject.get()
        if subject_value:
            log_button.config(state=tk.NORMAL)
        else:
            log_button.config(state=tk.DISABLED)

    for subject in subjects:
        Radiobutton(subject_frame, text=subject, variable=selected_subject, value=subject, font=("Arial", 12), bg='#ffeae6', command=on_subject_select).pack(anchor=tk.W)

    def on_log_attendance():
        subject_value = selected_subject.get()
        if subject_value:
            messagebox.showwarning("Face Visibility", "Remove all accessories that might cover your face and make sure your face is clearly visible.")
            success = log_attendance(subject_value)
            if success:
                root.destroy()  # Close the popup upon successful attendance logging
        else:
            messagebox.showwarning("Warning", "Please select a subject.")

    # Button to log attendance
    log_button = tk.Button(frame, text="Log Attendance", font=("Arial", 14), command=on_log_attendance, width=15, height=2, bg='#ffb6c1', state=tk.DISABLED)
    log_button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
