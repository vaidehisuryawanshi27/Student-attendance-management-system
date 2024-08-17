import tkinter as tk
from tkinter import PhotoImage, messagebox
import os
import subprocess
from PIL import Image, ImageTk

# Function to make window fullscreen
def make_fullscreen(event=None):
    state = not root.attributes("-fullscreen")
    root.attributes("-fullscreen", state)

# Function to open Register Student popup
def open_register_student():
    os.system('python register.py')

# Function to open Mark Attendance popup
def open_mark_attendance():
    process = subprocess.Popen(['python', 'attendance.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    
    if process.returncode != 0:
        messagebox.showerror("Error", f"An error occurred during marking attendance.\n{stderr.decode('utf-8')}")
    else:
        messagebox.showinfo("Mark Attendance", "Attendance process completed successfully.")

# Function to open Encode Faces and train LBPH model
def open_encode_faces():
    global encode_faces_button
    
    # Disable the Encode Faces button during encoding
    encode_faces_button.config(state=tk.DISABLED)
    
    # Show the message box before starting the subprocess
    messagebox.showinfo("Encoding Faces", "Encoding faces. This may take some time...")
    
    # Call encode.py using subprocess to run it in the background
    process = subprocess.Popen(['python', 'C:/Users/Vaidehi Suryawanshi/Downloads/Student Attendance (1)/Student Attendance/encode.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    
    # Display output from encode.py
    if process.returncode != 0:
        error_message = stderr.decode('utf-8')
        print(f"Error: {error_message}")  # Debugging information
        messagebox.showerror("Error", f"An error occurred during encoding.\n{error_message}")
    else:
        success_message = stdout.decode('utf-8')
        print(f"Success: {success_message}")  # Debugging information
        messagebox.showinfo("Encoding Complete", "Finished encoding.")
    
    # Enable the Encode Faces button after encoding
    encode_faces_button.config(text="Encode Faces", state=tk.NORMAL)

# Create the main window
root = tk.Tk()
root.title("Student Image Capture and Recognition")

# Set the window to start maximized
root.state('zoomed')

# Load background image and resize it to fit the screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

img = Image.open("C:/Users/Vaidehi Suryawanshi/Downloads/Student Attendance (1)/Student Attendance/bg.jpg")
img = img.resize((screen_width, screen_height), resample=Image.LANCZOS)  # Use Image.LANCZOS for resizing
background_image = ImageTk.PhotoImage(img)

background_label = tk.Label(root, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Load button icons
register_icon = PhotoImage(file="C:/Users/Vaidehi Suryawanshi/Downloads/Student Attendance (1)/Student Attendance/register.png")
attendance_icon = PhotoImage(file="C:/Users/Vaidehi Suryawanshi/Downloads/Student Attendance (1)/Student Attendance/attendance.png")
encode_icon = PhotoImage(file="C:/Users/Vaidehi Suryawanshi/Downloads/Student Attendance (1)/Student Attendance/encode.png")

# Button dimensions in cm
button_size_cm = 6  # Make buttons larger
button_size_px = int(button_size_cm * 37.7952755906)  # 1 cm ≈ 37.8 pixels

# Function to handle fullscreen and escape
root.bind("<F11>", make_fullscreen)
root.bind("<Escape>", lambda event: root.attributes("-fullscreen", False))

# Calculate button positions
button_spacing = 40  # Adjust as needed
button_start_x = (screen_width - (3 * button_size_px + 2 * button_spacing)) // 2
button_start_y = (screen_height - button_size_px) // 2

# Create and place the buttons for register, mark attendance, and encode faces
register_button = tk.Button(root, image=register_icon, text="Register Student", compound=tk.TOP, command=open_register_student, width=button_size_px, height=button_size_px, font=("Arial", 14), bg="#FFB6C1")
register_button.place(x=button_start_x, y=button_start_y)

attendance_button = tk.Button(root, image=attendance_icon, text="Mark Attendance", compound=tk.TOP, command=open_mark_attendance, width=button_size_px, height=button_size_px, font=("Arial", 14), bg="#FFB6C1")
attendance_button.place(x=button_start_x + button_size_px + button_spacing, y=button_start_y)

encode_faces_button = tk.Button(root, image=encode_icon, text="Encode Faces", compound=tk.TOP, command=open_encode_faces, width=button_size_px, height=button_size_px, font=("Arial", 14), bg="#FFB6C1")
encode_faces_button.place(x=button_start_x + 2 * (button_size_px + button_spacing), y=button_start_y)

# Run the application
root.mainloop()
