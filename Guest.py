import socket
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from jsonrpclib import Server

conn = Server('http://10.1.123.85:2509')

def G_main(callback_function):
    # Create the Tkinter window
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
    top_image = ImageTk.PhotoImage(top_image)

    # Create a label to display the top center image
    top_image_label = tk.Label(root, image=top_image)
    top_image_label.image = top_image
    top_image_label.pack(side="top", pady=10)

    # Load the icon image
    icon_image = Image.open('logo bold.png')  # Replace 'path_to_your_icon_image.png' with the actual path
    icon_image = icon_image.resize((120, 80))  # Adjust the size as needed
    icon_image = ImageTk.PhotoImage(icon_image)

    # Create a label to display the icon image in the right bottom corner
    icon_label = tk.Label(root, image=icon_image)
    icon_label.image = icon_image  # To prevent image from being garbage collected
    icon_label.pack(side="right", anchor="se", padx=10, pady=10)

    # Load the icon image
    icon_image2 = Image.open('LW1.png')  # Replace 'path_to_your_icon_image.png' with the actual path
    icon_image2 = icon_image2.resize((120, 80))  # Adjust the size as needed
    icon_image2 = ImageTk.PhotoImage(icon_image2)

    # Create a label to display the icon image in the left bottom corner
    icon_label2 = tk.Label(root, image=icon_image2)
    icon_label2.image = icon_image2  # To prevent image from being garbage collected
    icon_label2.pack(side="left", anchor="sw", padx=10, pady=10)

    # Create and pack widgets
    label = ttk.Label(root, text="Enter Staff ID / Register Number:")
    label.pack(pady=10)

    global reg_number_entry
    reg_number_entry = ttk.Entry(root)
    reg_number_entry.pack(pady=10)

    def send_info():
        id = reg_number_entry.get()
        if not id.strip():  # Check if the entry is empty or contains only whitespace
            messagebox.showerror("Error", "ID should not be empty.")
            return
        response = conn.guest_login(id, socket.gethostname())
        submit_button.config(state=tk.DISABLED)
        messagebox.showinfo('Guest Login', response)

    def end_guest():
        root.destroy()
        callback_function("")

    submit_button = ttk.Button(root, text="Submit", command=send_info)
    submit_button.pack(pady=10)

    end_button = ttk.Button(root, text="End Session", command=end_guest)
    end_button.pack(pady=11)


    # Run the Tkinter event loop'
    root.title("Guest Login")
    root.iconbitmap('256a.ico')
    root.mainloop()

if __name__ == "__main__":
    G_main()
