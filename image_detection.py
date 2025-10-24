import tkinter as tk
from tkinter import ttk
from PIL import ImageGrab, ImageTk
import torch
from torchvision import models, transforms
from torchvision.models import ResNet50_Weights
import requests

# Load model
model = models.resnet50(weights=ResNet50_Weights.DEFAULT)
model.eval()

# Labels
LABELS_URL = "https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt"
labels = [line.strip() for line in requests.get(LABELS_URL).text.splitlines()]

# Transform
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

class SnipApp:
    def __init__(self, master):
        self.master = master
        self.master.title("AI Snipping Tool")
        self.master.geometry("500x400")

        # Toolbar
        toolbar = ttk.Frame(master)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        ttk.Button(toolbar, text="New Snip", command=self.start_snip).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(toolbar, text="Exit", command=master.quit).pack(side=tk.LEFT, padx=5, pady=5)

        # Image preview
        self.preview_label = tk.Label(master)
        self.preview_label.pack(pady=10)

        # Status bar
        self.status = tk.StringVar()
        self.status.set("Ready")
        status_bar = ttk.Label(master, textvariable=self.status, relief=tk.SUNKEN, anchor="w")
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def start_snip(self):
        self.status.set("Select an area...")
        self.master.withdraw()  # Hide main window
        SnipWindow(self)

    def show_result(self, img, label):
        tk_img = ImageTk.PhotoImage(img)
        self.preview_label.configure(image=tk_img)
        self.preview_label.image = tk_img

        self.status.set(f"Detected: {label}")

        # Resize window to match image size + some padding
        w, h = img.size
        self.master.geometry(f"{w + 50}x{h + 100}")
        self.master.deiconify()

class SnipWindow:
    def __init__(self, app):
        self.app = app
        self.root = tk.Toplevel()
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-alpha", 0.3)
        self.canvas = tk.Canvas(self.root, cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.start_x = None
        self.start_y = None
        self.rect = None

        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

    def on_press(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red')

    def on_drag(self, event):
        cur_x = self.canvas.canvasx(event.x)
        cur_y = self.canvas.canvasy(event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_release(self, event):
        x1 = int(min(self.start_x, event.x))
        y1 = int(min(self.start_y, event.y))
        x2 = int(max(self.start_x, event.x))
        y2 = int(max(self.start_y, event.y))

        self.root.destroy()

        img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        label = self.detect(img)
        self.app.show_result(img, label)

    def detect(self, img):
        input_tensor = transform(img).unsqueeze(0)
        with torch.no_grad():
            outputs = model(input_tensor)
        _, predicted = outputs.max(1)
        return labels[predicted.item()]

if __name__ == "__main__":
    root = tk.Tk()
    app = SnipApp(root)
    root.mainloop()
