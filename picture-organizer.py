"""
Simple program that takes a folder, cycles through the images in it,
and moves the images to another folder
Pressing a key on the keyboard (latin) will move the image to the folder:
TARGET_FOLDER\key\
"""
from PIL import Image, ImageTk #python -m pip install Pillow
import os
import tkinter
import shutil
import argparse

def prepare_image(path : str)-> ImageTk:
    img = ImageTk.PhotoImage(Image.open(path))
    return img



class Viewer:
    def __init__(self, FOLDER, TARGET_FOLDER):
        self.FOLDER = FOLDER
        self.TARGET_FOLDER = TARGET_FOLDER
        self.window = None
        self.frame = None
        self.current_img : str = None
        self.img_list = []
        self.index = 0
        self.pressed_keys : dict = {}

        self.img_list = self.get_img_list(folder = FOLDER)
        self.current_img = self.img_list[self.index]

        window = tkinter.Tk()
        window.geometry("800x900")
        window.title("Hello")
        window.bind("<KeyRelease>", self.read_key)

        self.window = window
    
        frame = tkinter.Frame(window, width=600, height=400)
        frame.pack()
        frame.place(anchor='center', relx=0.5, rely=0.5)
        self.frame = frame

        self.load_img()
        self.window.mainloop()
    
    @classmethod
    def get_img_list(self, folder):
        files = [os.path.join(folder, f) for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
        f : str
        pictures = [f for f in files if str(f).endswith((".png",".jpg",".jpeg"))]
        return pictures

    def next(self):
        """Moves on to the next picture"""
        self.index += 1
        self.current_img = self.img_list[self.index]
        self.load_img()

    @classmethod
    def move_picture(self, path_input, target_folder):
        """
        copies path_input into target_folder
        """
        if not os.path.isdir(target_folder):
            os.makedirs(target_folder)
        dest = shutil.move(src = path_input, dst = target_folder)
        return dest

    def read_key(self, event):
        """Reads the pressed key and moves the current picture to the assigned folder
        TODO: have each key be defined by a different folder beforehand
        """
        key = str(event.char)
        print(key, str(self.current_img).encode('utf-8') )
        Viewer.move_picture(path_input = self.current_img,
                            target_folder = os.path.join(self.TARGET_FOLDER, key))
        self.pressed_keys[key] = 1
        self.next()


    def load_img(self):
        """
        Reloads the tkinter frame to show the next picture
        """
        image = Image.open(self.current_img)
        img = ImageTk.PhotoImage(image)
        for widget in self.frame.winfo_children():
            widget.destroy()
        tkinter.Label(self.frame, text = list(self.pressed_keys.keys())).pack()

        label = tkinter.Label(self.frame, image = img)
        label.pack()

        self.img = img



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', "--folder")  
    parser.add_argument('-tf', "--targetfolder")  

    #USE : python .\picture-organizer.py -f "path\to\picturefolder" -tf "path\to\targetfolder"

    args = parser.parse_args()
    folder = args.folder
    targetfolder = args.targetfolder

    vw = Viewer(FOLDER = folder, TARGET_FOLDER = targetfolder)
   


