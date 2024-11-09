import tkinter as tk
from tkinter import filedialog, Text
from PIL import Image, ImageTk
import pytesseract

# Specify path to Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Initialize the main application window
root = tk.Tk()
root.title("OCRos")
root.geometry("700x500")

# Variables to store image and cropping coordinates
uploaded_image_path = None
original_image = None
cropped_image = None
start_x = start_y = end_x = end_y = 0

# Function to upload an image and display it in the window
def upload_image():
    global uploaded_image_path, original_image, cropped_image
    uploaded_image_path = filedialog.askopenfilename(filetypes=[("Pliki graficzne", "*.png;*.jpg;*.jpeg")])

    if uploaded_image_path:
        original_image = Image.open(uploaded_image_path)
        cropped_image = original_image.copy()
        show_image(original_image)

        # Enable the canvas for cropping
        img_canvas.bind("<ButtonPress-1>", on_button_press)
        img_canvas.bind("<B1-Motion>", on_mouse_drag)
        img_canvas.bind("<ButtonRelease-1>", on_button_release)
        extract_btn.config(state="normal")

# Function to show the image on the canvas
def show_image(image):
    img = image.copy()
    img.thumbnail((300, 300))
    img_tk = ImageTk.PhotoImage(img)

    img_canvas.config(width=img.width, height=img.height)
    img_canvas.create_image(0, 0, anchor="nw", image=img_tk)
    img_canvas.image = img_tk

# Mouse events for cropping
def on_button_press(event):
    global start_x, start_y
    start_x, start_y = event.x, event.y
    img_canvas.delete("crop_rectangle")

def on_mouse_drag(event):
    global end_x, end_y
    end_x, end_y = event.x, event.y
    img_canvas.delete("crop_rectangle")
    img_canvas.create_rectangle(start_x, start_y, end_x, end_y, outline="red", tag="crop_rectangle")

def on_button_release(event):
    global end_x, end_y
    end_x, end_y = event.x, event.y
    # Adjust crop area to be within image bounds
    end_x = max(0, min(end_x, img_canvas.winfo_width()))
    end_y = max(0, min(end_y, img_canvas.winfo_height()))

# Helper function for calculating crop coordinates
def calculate_crop_box(start_x, start_y, end_x, end_y, img_width, img_height, canvas_width, canvas_height):
    # Ensure coordinates are ordered correctly
    left = min(start_x, end_x)
    right = max(start_x, end_x)
    top = min(start_y, end_y)
    bottom = max(start_y, end_y)

    # Convert canvas coordinates to the original image's scale
    scale_x = img_width / canvas_width
    scale_y = img_height / canvas_height

    crop_box = (
        int(left * scale_x),
        int(top * scale_y),
        int(right * scale_x),
        int(bottom * scale_y),
    )
    return crop_box

# Function to crop the image based on selected rectangle
def apply_crop():
    global cropped_image
    if original_image:
        # Calculate the crop box in the scale of the original image
        crop_box = calculate_crop_box(start_x, start_y, end_x, end_y,
                                      original_image.width, original_image.height,
                                      img_canvas.winfo_width(), img_canvas.winfo_height())

        cropped_image = original_image.crop(crop_box)
        show_image(cropped_image)

# Function to perform OCR and display the text
def extract_text():
    if cropped_image:
        text = pytesseract.image_to_string(cropped_image, lang="pol")
        text_box.delete(1.0, tk.END)
        text_box.insert(tk.END, text)
    else:
        text_box.delete(1.0, tk.END)
        text_box.insert(tk.END, "Proszę załadować obraz i wybrać obszar.")

# Canvas to display the image and draw the cropping rectangle
img_canvas = tk.Canvas(root, cursor="cross")
img_canvas.pack(pady=10)

# Button to upload the image
upload_btn = tk.Button(root, text="Załaduj obraz", command=upload_image)
upload_btn.pack(pady=5)

# Button to apply the crop
apply_crop_btn = tk.Button(root, text="Zastosuj przycięcie", command=apply_crop, state="normal")
apply_crop_btn.pack(pady=5)

# Button to start OCR extraction
extract_btn = tk.Button(root, text="Wydobądź tekst", command=extract_text, state="disabled")
extract_btn.pack(pady=5)

# Textbox to display the OCR text
text_box = Text(root, wrap='word', height=10)
text_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

root.mainloop()
