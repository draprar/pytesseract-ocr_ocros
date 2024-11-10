import tkinter as tk
from tkinter import filedialog, Text, messagebox
from PIL import ImageTk
import ocros_logic


class OCRosApp:
    """Main application class for OCRos GUI."""

    def __init__(self, root):
        self.root = root
        self.root.title("OCRos")
        self.root.geometry("700x500")

        # Initialize variables
        self.uploaded_image_path = None
        self.original_image = None
        self.cropped_image = None
        self.start_x = self.start_y = self.end_x = self.end_y = 0
        self.rect_id = None  # ID for the rectangle drawn on canvas

        # Set up the UI
        self.setup_ui()

    def setup_ui(self):
        """Set up the user interface elements."""
        self.img_canvas = tk.Canvas(self.root, cursor="cross")
        self.img_canvas.pack(pady=10)

        self.upload_btn = tk.Button(self.root, text="Załaduj obraz", command=self.upload_image)
        self.upload_btn.pack(pady=5)

        self.apply_crop_btn = tk.Button(self.root, text="Zastosuj przycięcie", command=self.apply_crop, state="disabled")
        self.apply_crop_btn.pack(pady=5)

        self.extract_btn = tk.Button(self.root, text="Wydobądź tekst", command=self.extract_text, state="disabled")
        self.extract_btn.pack(pady=5)

        self.text_box = Text(self.root, wrap='word', height=10)
        self.text_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Bind mouse events for cropping functionality
        self.img_canvas.bind("<ButtonPress-1>", self.on_mouse_press)
        self.img_canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.img_canvas.bind("<ButtonRelease-1>", self.on_mouse_release)

    def upload_image(self):
        """Handle image upload and display."""
        self.uploaded_image_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")]
        )
        if not self.uploaded_image_path:
            return

        try:
            self.original_image = ocros_logic.load_image(self.uploaded_image_path)
            self.cropped_image = self.original_image.copy()
            self.show_image(self.original_image)
            self.apply_crop_btn.config(state="normal")
            self.extract_btn.config(state="normal")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {e}")

    def show_image(self, image):
        """Display image on the canvas."""
        img = image.copy()
        img.thumbnail((300, 300))
        img_tk = ImageTk.PhotoImage(img)
        self.img_canvas.config(width=img.width, height=img.height)
        self.img_canvas.create_image(0, 0, anchor="nw", image=img_tk)
        self.img_canvas.image = img_tk

    def on_mouse_press(self, event):
        """Store the starting position of the cropping rectangle."""
        self.start_x, self.start_y = event.x, event.y
        if self.rect_id:
            self.img_canvas.delete(self.rect_id)
        self.rect_id = None

    def on_mouse_drag(self, event):
        """Draw the cropping rectangle on the canvas."""
        self.end_x, self.end_y = event.x, event.y
        if self.rect_id:
            self.img_canvas.delete(self.rect_id)
        self.rect_id = self.img_canvas.create_rectangle(
            self.start_x, self.start_y, self.end_x, self.end_y, outline="red", width=2
        )

    def on_mouse_release(self, event):
        """Finalize the cropping coordinates."""
        self.end_x, self.end_y = event.x, event.y
        if self.rect_id:
            self.img_canvas.delete(self.rect_id)
        self.rect_id = self.img_canvas.create_rectangle(
            self.start_x, self.start_y, self.end_x, self.end_y, outline="red", width=2
        )

    def apply_crop(self):
        """Crop the selected image region and display it."""
        if self.original_image:
            crop_box = ocros_logic.calculate_crop_box(
                self.start_x, self.start_y, self.end_x, self.end_y,
                self.original_image.width, self.original_image.height,
                self.img_canvas.winfo_width(), self.img_canvas.winfo_height()
            )
            self.cropped_image = ocros_logic.crop_image(self.original_image, crop_box)
            self.show_image(self.cropped_image)

    def extract_text(self):
        """Extract text from the cropped image and display it in the text box."""
        if self.cropped_image:
            text = ocros_logic.extract_text_from_image(self.cropped_image, lang="pol").strip()
            self.text_box.delete(1.0, tk.END)
            self.text_box.insert(tk.END, text)


if __name__ == "__main__":
    root = tk.Tk()
    app = OCRosApp(root)
    root.mainloop()
