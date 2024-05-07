import threading
import tkinter as tk
from tkinter import ttk, messagebox
from UI_Clinet import create_attendance_ui
from Guest import G_main
from PIL import Image, ImageTk
import socket
import schedule
import time
from datetime import datetime, time as dt_time


period_timings = [
    {"name": "Hour 1", "start_time": dt_time(8, 30, 1), "end_time": dt_time(9, 20)},
    {"name": "Hour 2", "start_time": dt_time(9, 20, 1), "end_time": dt_time(10, 10)},
    {"name": "Hour 3", "start_time": dt_time(10, 10, 1), "end_time": dt_time(11, 0)},
    {"name": "Hour 4", "start_time": dt_time(11, 0, 1), "end_time": dt_time(11, 50)},
    {"name": "Hour 5", "start_time": dt_time(11, 50, 1), "end_time": dt_time(12, 40)},
    {"name": "Hour 6", "start_time": dt_time(12, 40, 1), "end_time": dt_time(13, 30)},
    {"name": "Hour 7", "start_time": dt_time(13, 30, 1), "end_time": dt_time(14, 15)},
    {"name": "Hour 8", "start_time": dt_time(14, 15, 1), "end_time": dt_time(15, 0)},
    {"name": "Hour 9", "start_time": dt_time(15, 0, 1), "end_time": dt_time(15, 45)},
]

root = None
schedule_received = False


def handle_attendance_response(response):
    main()


def create_client_Ui():
    global root
    root = tk.Tk()

    # Disable the close button
    root.protocol("WM_DELETE_WINDOW", lambda: None)
    # Disable the maximize button
    root.resizable(False, False)

    # Set the window size and position in the center of the screen
    window_width = 500  # Adjust the width as needed
    window_height = 300  # Adjust the height as needed

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Load the top center image
    top_image = Image.open('srm new.png')  # Replace with the actual path
    top_image = top_image.resize((150, 75))
    top_image_tk = ImageTk.PhotoImage(top_image)

    # Create a label to display the top center image
    top_image_label = tk.Label(root, image=top_image_tk)
    top_image_label.image = top_image_tk
    top_image_label.pack(side="top", pady=10)

    # Load the icon image
    icon_image = Image.open('logo bold.png')  # Replace 'path_to_your_icon_image.png' with the actual path
    icon_image = icon_image.resize((120, 80))  # Adjust the size as needed
    icon_image_tk = ImageTk.PhotoImage(icon_image)

    # Create a label to display the icon image in the right bottom corner
    icon_label = tk.Label(root, image=icon_image_tk)
    icon_label.image = icon_image_tk  # To prevent image from being garbage collected
    icon_label.pack(side="right", anchor="se", padx=10, pady=10)

    # Load the icon image
    icon_image2 = Image.open('LW1.png')  # Replace 'path_to_your_icon_image.png' with the actual path
    icon_image2 = icon_image2.resize((120, 80))  # Adjust the size as needed
    icon_image2_tk = ImageTk.PhotoImage(icon_image2)

    # Create a label to display the icon image in the left bottom corner
    icon_label2 = tk.Label(root, image=icon_image2_tk)
    icon_label2.image = icon_image2_tk  # To prevent image from being garbage collected
    icon_label2.pack(side="left", anchor="sw", padx=10, pady=10)

    # Create a label and two radio buttons
    label = ttk.Label(root, text="Select User Type :", font=("Georgia", 12, "bold"))
    label.pack(padx=10, pady=10)
    user_type_var = tk.StringVar()
    student_radio = ttk.Radiobutton(root, text="Student", variable=user_type_var, value="Student",
                                    style="Bold.TRadiobutton")
    student_radio.pack(padx=10, pady=5)

    staff_radio = ttk.Radiobutton(root, text="Guest    ", variable=user_type_var, value="Guest",
                                  style="Bold.TRadiobutton")
    staff_radio.pack(padx=10, pady=5)

    def submit_user_type():
        user_type = user_type_var.get()
        if user_type:
            if user_type == "Student":
                root.destroy()
                create_attendance_ui(handle_attendance_response, period_timings)
            elif user_type == "Guest":
                root.destroy()
                G_main(handle_attendance_response)
        else:
            messagebox.showerror("Error", "Please select a user type.")

    submit_button = ttk.Button(root, text="Submit", command=submit_user_type)
    submit_button.pack(pady=10)

    root.title("User Login")
    root.iconbitmap('256a.ico')
    root.mainloop()


def main():
    create_client_Ui()


if __name__ == "__main__":
    main()
