import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os


def load_images():
    global ORIGINAL_IMAGE, BINARIZED_IMAGE, image_path, files, current_image_index, folder_path
    # Get the selected folder
    folder_path = filedialog.askdirectory(
        title="Select Folder", initialdir=os.getcwd())
    print(folder_path)
    if folder_path:
        # Get all files in the folder which are images
        files = [file for file in os.listdir(
            folder_path) if file.endswith(("png", "jpg", "jpeg"))]

        # Load the first image
        if files:
            current_image_index = 0
            image_path = os.path.join(folder_path, files[current_image_index])
            load_image(image_path)


def load_single_image():
    global ORIGINAL_IMAGE, BINARIZED_IMAGE, image_path, files, current_image_index
    file_path = filedialog.askopenfile(
        title="Select an image", initialdir=os.getcwd()
    )
    print(file_path)
    if file_path:
        image_path = file_path
        load_image(image_path)


def load_image(path):
    global ORIGINAL_IMAGE, BINARIZED_IMAGE

    ORIGINAL_IMAGE = Image.open(path).convert("L")
    BINARIZED_IMAGE = binarize_image(ORIGINAL_IMAGE)

    original_ph = ImageTk.PhotoImage(ORIGINAL_IMAGE)
    original_img_label.configure(image=original_ph)
    original_img_label.image = original_ph

    binarized_ph = ImageTk.PhotoImage(BINARIZED_IMAGE)
    binarized_img_label.configure(image=binarized_ph)
    binarized_img_label.image = binarized_ph


def binarize_image(image, threshold=128):
    # Get the threshold value
    # threshold = int(range_var.get())

    # Binarize the image
    binarized_image = image.point(
        lambda pixel: 255 if pixel > threshold else 0)

    return binarized_image


def save_binarized_image():
    global BINARIZED_IMAGE, image_path

    if BINARIZED_IMAGE:
        # Create the 'binarized' directory if it doesn't exist
        output_dir = os.path.join(os.path.dirname(image_path), "binarized")
        os.makedirs(output_dir, exist_ok=True)

        # Save the binarized image in the 'binarized' directory
        print(image_path)
        output_path = os.path.join(
            output_dir, "binarized_" + os.path.basename(image_path))
        BINARIZED_IMAGE.save(output_path)
        print("Binarized image saved:", output_path)


def change_range_value(value):
    global ORIGINAL_IMAGE, BINARIZED_IMAGE  # Declare global variables
    if ORIGINAL_IMAGE:
        BINARIZED_IMAGE = binarize_image(ORIGINAL_IMAGE, int(value))

        binarized_ph = ImageTk.PhotoImage(BINARIZED_IMAGE)
        binarized_img_label.configure(image=binarized_ph)
        binarized_img_label.image = binarized_ph


def next_image():
    global current_image_index, files, folder_path, image_path
    if current_image_index < len(files) - 1:
        current_image_index += 1
        image_path = os.path.join(folder_path, files[current_image_index])
        load_image(image_path)


# Create the Tkinter app window
window = tk.Tk()
window.title("Image Binarization")
window.geometry("1000x700")

# Button to select folder and load images
load_button = tk.Button(window, text="Select Folder", command=load_images)
# load_button = tk.Button(window, text="Select Image", command=load_single_image)
load_button.pack()

# Single pointer range for threshold value
range_label = tk.Label(window, text="Threshold Value:")

range_var = tk.DoubleVar()
range_scale = tk.Scale(window, variable=range_var, from_=0,
                       to=255, orient=tk.HORIZONTAL, command=change_range_value)
# give the scale full width
range_scale.pack(fill=tk.X, padx=10)
range_var.set(127)
range_var.trace("w", change_range_value)
range_scale.pack()


# Label for original image
original_label = tk.Label(window, text="Original Image")
original_label.pack(anchor='center')

# Original image viewer
original_img_label = tk.Label(window, width=700, height=250)
original_img_label.pack()

# Label for binarized image
binarized_label = tk.Label(window, text="Binarized Image")
binarized_label.pack()

# Binarized image viewer
binarized_img_label = tk.Label(window, width=700, height=250)
binarized_img_label.pack()

# Button to save binarized image
save_button = tk.Button(window, text="Save Binarized",
                        command=save_binarized_image)
save_button.pack(pady=10)

# Next image button
next_button = tk.Button(window, text="Next Image", command=next_image)
next_button.pack(pady=10)

# Run the Tkinter event loop
window.mainloop()
