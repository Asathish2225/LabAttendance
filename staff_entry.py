import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk
import pandas as pd
import tkinter.messagebox as messagebox
import Client
import main_server

root = None


class AutocompleteCombobox(ttk.Combobox):
    def set_completion_list(self, completion_list):
        # Convert all items to strings before sorting
        self._completion_list = sorted(map(str, completion_list))
        self._hits = []
        self.position = 0
        self.bind('<KeyRelease>', self.handle_keyrelease)
        self['values'] = self._completion_list

    def autocomplete(self, delta=0):
        if delta:
            self.delete(0, tk.END)
        else:
            self.delete(self.index(tk.END) - 1)

        current_text = self.get().lower()
        _hits = [item for item in self._completion_list if item.lower().startswith(current_text)]
        _hits = sorted(_hits)

        if _hits != self._hits:
            self._hits = _hits
            self.position = 0
            self['values'] = self._hits
            self.event_generate('<Down>')

    def set_var(self, var):
        self.var = var

    def handle_keyrelease(self, event):
        if event.keysym in ('BackSpace', 'Left', 'Right', 'Up', 'Down', 'Shift_R', 'Shift_L', 'Control_R', 'Control_L'):
            return
        if event.keysym in ('Return', 'KP_Enter'):
            self.set_completion()
            return

        self.autocomplete()

    def set_completion(self):
        if self.var.get() not in self._completion_list:
            self._completion_list.append(self.var.get())
            self._completion_list = sorted(self._completion_list)
            self['values'] = self._completion_list


def update_subject_dropdown():
    selected_staff = staff_incharge_var.get()
    if selected_staff:
        # Filter subjects based on the selected staff incharge
        subjects_str = df[df.iloc[:, 1] == selected_staff].iloc[:, 2].tolist()
        subjects_list = [subject.strip() for subjects in subjects_str for subject in subjects.split(',')]

        # If there's only one subject, set it as the fixed value
        if len(subjects_list) == 1:
            subject_var.set(subjects_list[0])
            subject_dropdown['values'] = subjects_list
        else:
            subject_dropdown['values'] = subjects_list
    else:
        subject_dropdown.set("")


def update_Class_dropdown():
    selected_staff = staff_incharge_var.get()
    if selected_staff:
        # Filter Classes based on the selected staff incharge
        Class_str = df[df.iloc[:, 1] == selected_staff].iloc[:, 3].tolist()
        Class_list = [Class.strip() for Classes in Class_str for Class in Classes.split(',')]

        # If there's only one class, set it as the fixed value
        if len(Class_list) == 1:
            Class_var.set(Class_list[0])
            Class_dropdown['values'] = Class_list
        else:
            Class_dropdown['values'] = Class_list
    else:
        Class_dropdown.set("")


def on_submit():
    selected_staff = staff_incharge_var.get()
    selected_subject = subject_var.get()
    selected_class = Class_var.get()

    if selected_staff == "Select Staff Incharge" or selected_subject == "Select Subject" or selected_class == "Select Class":
        # Show an error message box if any dropdown has the default value
        messagebox.showerror("Error", "Please select options for all dropdowns.")
    else:
        print(f"Submitted - Staff: {selected_staff}, Subject: {selected_subject}, Class: {selected_class}")
        assign()
        root.destroy()


def assign():
    main_server.staff = staff_incharge_var.get()
    main_server.subject = subject_var.get()
    main_server.Class = Class_var.get()


def main():
    main_server.staff = ""
    main_server.subject = ""
    main_server.Class = ""

    global root
    root = tk.Tk()

    window_width = 500
    window_height = 300

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    top_image = Image.open('srm new.png')
    top_image = top_image.resize((150, 75))
    top_image = ImageTk.PhotoImage(top_image)

    top_image_label = tk.Label(root, image=top_image)
    top_image_label.image = top_image
    top_image_label.pack(side="top", pady=10)

    icon_image = Image.open('logo bold.png')
    icon_image = icon_image.resize((120, 80))
    icon_image = ImageTk.PhotoImage(icon_image)

    icon_label = tk.Label(root, image=icon_image)
    icon_label.image = icon_image
    icon_label.pack(side="right", anchor="se", padx=10, pady=10)

    icon_image2 = Image.open('LW1.png')
    icon_image2 = icon_image2.resize((120, 80))
    icon_image2 = ImageTk.PhotoImage(icon_image2)

    icon_label2 = tk.Label(root, image=icon_image2)
    icon_label2.image = icon_image2
    icon_label2.pack(side="left", anchor="sw", padx=10, pady=10)

    # Read staff names from Excel file
    excel_file_path = "C:\\Attendance\\LAB ROOM WITH STAFF DATA.xlsx"  # Replace with the path to your Excel file
    global df
    df = pd.read_excel(excel_file_path)

    global staff_incharge
    staff_incharge = df.iloc[:, 1].tolist()

    global staff_incharge_var
    staff_incharge_var = tk.StringVar(root)
    staff_incharge_var.set("Select Staff Incharge")

    global staff_incharge_dropdown
    staff_incharge_dropdown = AutocompleteCombobox(root, textvariable=staff_incharge_var)
    staff_incharge_dropdown.set_completion_list(staff_incharge)
    staff_incharge_dropdown.pack(pady=10)

    staff_incharge_dropdown.bind('<ButtonRelease>', lambda event: update_subject_dropdown())
    staff_incharge_dropdown.bind('<<ComboboxSelected>>', lambda event: (update_subject_dropdown(), update_Class_dropdown()))

    # Class dropdown
    global Class_var
    Class_var = tk.StringVar(root)
    Class_var.set("Select Class")

    global Class_dropdown
    Class_dropdown = ttk.Combobox(root, textvariable=Class_var, state="readonly")
    Class_dropdown.pack(pady=10)

    Class_dropdown.bind('<FocusIn>', lambda event: update_Class_dropdown())
    Class_dropdown.bind('<<ComboboxSelected>>', lambda event: assign())

    # Subject dropdown
    global subject_var
    subject_var = tk.StringVar(root)
    subject_var.set("Select Subject")

    global subject_dropdown
    subject_dropdown = ttk.Combobox(root, textvariable=subject_var, state="readonly")
    subject_dropdown.pack(pady=10)

    subject_dropdown.bind('<FocusIn>', lambda event: update_subject_dropdown())
    subject_dropdown.bind('<<ComboboxSelected>>', lambda event: update_Class_dropdown())

    # Submit button
    submit_button = tk.Button(root, text="Submit", command=on_submit)
    submit_button.pack(pady=10)

    root.title("Staff Entry")
    root.iconbitmap('256a.ico')

    root.title("Staff Entry")
    root.iconbitmap('256a.ico')
    root.mainloop()

if __name__ == "__main__":
    main()
