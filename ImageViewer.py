import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import os

class ImageViewer:
    def __init__(self, master):
        self.master = master
        self.master.title("Python Simple Image Viewer")
        self.master.geometry("600x600")

        self.delete = r"/delete"
        self.clg = r"/clg"
        self.fam = r"/fam"
        self.myself = r"/myself"
        self.interesting = r"/interesting"

        self.top_frame = tk.Frame(self.master, width=600, bd=1, relief="solid")
        self.top_frame.pack(side="top", fill="both", expand="yes")

        self.mid_frame = tk.Frame(self.master, width=300, height=200, bd=1, relief="solid")
        self.mid_frame.pack(side="top")

        self.images = []
        self.location = 0

        self.lbl_title = tk.Label(self.top_frame, text="Label", font=("Arial", 20))
        self.lbl_title.pack()

        self.forward = tk.Button(self.top_frame, text="Forward", command=lambda: self.load_image(1))
        self.forward.pack(side="left")

        self.back = tk.Button(self.top_frame, text="Back", command=lambda: self.load_image(-1))
        self.back.pack(side="left")

        self.print_location = tk.Button(self.top_frame, text="Print Location", command=self.locator)
        self.print_location.pack(side="left")

        self.parse_folder()

        # Binding keys
        master.focus_force()
        self.master.bind('<Left>', lambda event: self.back_action())
        self.master.bind('p', lambda event: self.locator())
        self.master.bind('<Right>', lambda event: self.forward_action())
        self.master.bind('s', lambda event: self.move_to_other_directory('s'))
        self.master.bind('f', lambda event: self.move_to_other_directory('f'))
        self.master.bind('d', lambda event: self.move_to_other_directory('d'))
        self.master.bind('c', lambda event: self.move_to_other_directory('c'))

    def parse_folder(self):
        file_path = filedialog.askdirectory()
        if not file_path:
            messagebox.showerror("Error", "No folder selected.")
            return

        try:
            for file in os.listdir(file_path):
                if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".png"):
                    self.images.append(os.path.join(file_path, file))
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        if not self.images:
            messagebox.showerror("Error", "No images found in the selected folder.")
            return

        self.load_image(0)
        self.assign_paths(path=file_path)

    def load_image(self, direction):
        self.location += direction
        if self.location >= len(self.images):
            self.location = 0
        elif self.location < 0:
            self.location = len(self.images) - 1

        image = Image.open(self.images[self.location])
        image = image.resize((900, 600), Image.LANCZOS)
        image = ImageTk.PhotoImage(image)

        self.lbl_title.config(image=image)
        self.lbl_title.image = image

    def assign_paths(self, path):
        self.delete = path + self.delete
        self.clg = path + self.clg
        self.fam = path + self.fam
        self.myself = path + self.myself
        self.interesting = path + self.interesting

        if(not os.path.exists(self.delete)):
            os.mkdir(self.delete)
        if(not os.path.exists(self.clg)):
            os.mkdir(self.clg)
        if(not os.path.exists(self.fam)):
            os.mkdir(self.fam)
        if(not os.path.exists(self.myself)):
            os.mkdir(self.myself)
        if(not os.path.exists(self.interesting)):
            os.mkdir(self.interesting)

    def locator(self):
        print(self.images[self.location])

    def back_action(self):
        self.load_image(-1)
    
    def forward_action(self):
        self.load_image(1)

    def move_and_delete(self, pathToDelete):
        self.load_image(0)
        self.images.remove(pathToDelete)

    def move_to_other_directory(self, dir_type):
        current_path = self.images[self.location]
        current_filename = r"/" + os.path.basename(current_path)
        previous_location = self.location
        
        match(dir_type):
            case 's':
                self.move_and_delete(current_path)
                os.rename(src=current_path, dst=self.myself+current_filename)
            case 'd':
                self.move_and_delete(current_path)
                os.rename(src=current_path, dst=self.delete+current_filename)
            case 'f':
                self.move_and_delete(current_path)
                os.rename(src=current_path, dst=self.fam+current_filename)
            case 'c':
                self.move_and_delete(current_path)
                os.rename(src=current_path, dst=self.clg+current_filename)
            case 'i':
                self.move_and_delete(current_path)
                os.rename(src=current_path, dst=self.interesting+current_filename)

if __name__ == "__main__":
    root = tk.Tk()
    viewer = ImageViewer(root)
    root.mainloop()


# doing for just a test
print(test)
