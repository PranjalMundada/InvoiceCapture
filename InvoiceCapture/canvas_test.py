# -*- coding: utf-8 -*-

import tkinter as tk

# --- functions ---

def on_click():
    # change image on canvas
    canvas.itemconfig(image_id, image=image2)

# --- main ---

root = tk.Tk()

# canvas for image
canvas = tk.Canvas(root, width=600, height=600)
canvas.pack()

# button to change image
button = tk.Button(root, text="Change", command=on_click)
button.pack()

# images
image1 = tk.PhotoImage(file="attachments/invoice.png")
image2 = tk.PhotoImage(file="res/images/handtext2.png")
print(image1.width())

canvas.config(width=image1.width(), height = image1.height())
# set first image on canvas
image_id = canvas.create_image(0, 0, anchor='nw', image=image1)


root.mainloop()