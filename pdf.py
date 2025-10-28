from tkinter import filedialog, messagebox
from PIL import Image
import os

try:
    from tkinterdnd2 import TkinterDnD, DND_FILES
    import tkinter as tk
except ImportError:
    import tkinter as tk
    DND_FILES = None  

class ImageToPDFApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image to PDF Converter")
        self.root.geometry("400x300")
        self.root.config(bg="#f2f2f2")

        self.images = []

        self.label = tk.Label(root, text="Glissez vos images ici 👇", bg="#f2f2f2", font=("Arial", 12))
        self.label.pack(pady=20)

        self.drop_area = tk.Label(root, text="Déposez les images ici", bg="#d9edf7", fg="#31708f",
                                  width=40, height=8, relief="ridge")
        self.drop_area.pack(pady=10)

        self.btn_select = tk.Button(root, text="📁 Sélectionner des images", command=self.select_files)
        self.btn_select.pack(pady=5)

        self.btn_convert = tk.Button(root, text="📄 Convertir en PDF", command=self.convert_to_pdf)
        self.btn_convert.pack(pady=10)

        if DND_FILES:
            self.root.drop_target_register(DND_FILES)
            self.root.dnd_bind('<<Drop>>', self.on_drop)
        else:
            messagebox.showwarning("Attention", "Glisser-déposer désactivé (tkinterdnd2 non installé).")

    def on_drop(self, event):
        files = self.root.tk.splitlist(event.data)
        for f in files:
            if f.lower().endswith(('.png', '.jpg', '.jpeg')):
                self.images.append(f)
        self.update_label()

    def select_files(self):
        files = filedialog.askopenfilenames(title="Sélectionner des images",
                                            filetypes=[("Images", "*.jpg *.jpeg *.png")])
        self.images.extend(files)
        self.update_label()

    def update_label(self):
        if self.images:
            filenames = [os.path.basename(f) for f in self.images]
            self.drop_area.config(text="\n".join(filenames[:5]) + ("\n..." if len(filenames) > 5 else ""))
        else:
            self.drop_area.config(text="Déposez les images ici")

    def convert_to_pdf(self):
        if not self.images:
            messagebox.showerror("Erreur", "Aucune image sélectionnée.")
            return

        output_path = filedialog.asksaveasfilename(defaultextension=".pdf",
                                                   filetypes=[("PDF files", "*.pdf")])
        if not output_path:
            return

        imgs = [Image.open(img).convert('RGB') for img in self.images]
        imgs[0].save(output_path, save_all=True, append_images=imgs[1:])
        messagebox.showinfo("Succès", f"PDF créé avec succès :\n{output_path}")

# Lancer l'app
if __name__ == "__main__":
    try:
        from tkinterdnd2 import TkinterDnD
        root = TkinterDnD.Tk()
    except ImportError:
        root = tk.Tk()
    app = ImageToPDFApp(root)
    root.mainloop()
