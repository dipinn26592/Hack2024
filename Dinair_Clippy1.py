import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk
from main import copilot

root = tk.Tk()
root.overrideredirect(True)
root.attributes('-topmost', True)
root.config(bg='white')
root.wm_attributes('-transparentcolor', 'white')

image = Image.open("assistant.png")
image = image.resize((100, 100), Image.LANCZOS)
assistant_img = ImageTk.PhotoImage(image)

assistant_label = Label(root, image=assistant_img, bg='white')
assistant_label.pack()

x_offset = 800
y_offset = 600

def start_move(event):
    global x_offset, y_offset
    x_offset = event.x
    y_offset = event.y

def move_window(event):
    new_x = event.x_root - x_offset
    new_y = event.y_root - y_offset
    root.geometry(f'+{new_x}+{new_y}')

def handle_double_click(event):
    copilot()

assistant_label.bind('<Button-1>', start_move)
assistant_label.bind('<B1-Motion>', move_window)
assistant_label.bind('<Double-1>', handle_double_click)

def close_app(event):
    root.quit()

assistant_label.bind('<Double-3>', close_app)  # Double-right-click to close the app

root.geometry("+100+100")
root.resizable(False, False)
root.mainloop()
