import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import filedialog
import cv2
import numpy as np

ctk.set_default_color_theme('green')

class App1(ctk.CTk):
    def __init__(self):
        super().__init__()
        self._set_appearance_mode('Dark')
        self.title('Edge Detection')
        self.geometry('1024x720')
        self.frame = ctk.CTkScrollableFrame(self, fg_color='#171717')
        self.frame.pack(padx=5, pady=5, fill='both', expand=True)
        self.dflt_fnt = ctk.CTkFont(family='arial', weight='bold')
        self.original_img = None
        self.processed_img_window = None
        self.add_buttons_sliders()

    def load_img(self):
        self.segButton.set(0)
        img_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif")])
        if img_path:
            self.original_img = cv2.imread(img_path)
            self.update_img(self.original_img)
        else:
            pass

    def update_img(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        fin_img = ctk.CTkImage(dark_image=img, size=img.size)
        self.image_label.configure(image=fin_img, text='')

    def reset_img(self):
        if self.original_img is not None:
            self.update_img(self.original_img)
            self.segButton.set(0)
            self.show_processed_img(self.original_img)
        else:
            pass

    def get_sgmntd_value(self, value):
        if self.original_img is not None:
            if value == 'Roberts':
                self.apply_roberts()
            elif value == 'Prewitt':
                self.apply_prewitt()
            elif value == 'Sobel':
                self.apply_sobel()
        else:
            self.segButton.set(0)

    def apply_sobel(self):
        gray_img = cv2.cvtColor(self.original_img, cv2.COLOR_BGR2GRAY)
        sobel_x = cv2.Sobel(gray_img, cv2.CV_64F, 1, 0, ksize=3)
        sobel_y = cv2.Sobel(gray_img, cv2.CV_64F, 0, 1, ksize=3)
        sobel_img = np.sqrt(sobel_x ** 2 + sobel_y ** 2)
        sobel_img = cv2.normalize(sobel_img, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        self.show_processed_img(sobel_img)

    def apply_prewitt(self):
        gray_img = cv2.cvtColor(self.original_img, cv2.COLOR_BGR2GRAY)
        img_gaussian = cv2.GaussianBlur(gray_img, (3, 3), 0)
        kernelx = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
        kernely = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]])
        img_prewittx = cv2.filter2D(img_gaussian, -1, kernelx)
        img_prewitty = cv2.filter2D(img_gaussian, -1, kernely)
        prewitt_img = abs(img_prewittx) + abs(img_prewitty)
        self.show_processed_img(prewitt_img)

    def apply_roberts(self):
        gray_img = cv2.cvtColor(self.original_img, cv2.COLOR_BGR2GRAY)
        roberts_img = cv2.Canny(gray_img, 100, 200)
        self.show_processed_img(roberts_img)

    def show_processed_img(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        fin_img = ctk.CTkImage(dark_image=img, size=img.size)
        w, h = img.size
        if self.processed_img_window is None or not self.processed_img_window.winfo_exists():
            self.processed_img_window = ctk.CTkToplevel(self)
            self.processed_img_window.title('Processed Image')
            self.processed_img_window.geometry(f'{str(w)}x{str(h)}')
            self.processed_image_label = ctk.CTkLabel(self.processed_img_window, text='')
            self.processed_image_label.pack(expand=True)

        self.processed_image_label.configure(image=fin_img, text='')

    def add_buttons_sliders(self):
        # Frame to contain the buttons
        button_frame = ctk.CTkFrame(self.frame, fg_color='#171717')
        button_frame.pack(pady=10)

        # Button To Browse a photo
        self.browse_button = ctk.CTkButton(button_frame, text="Browse Image", command=self.load_img, font=self.dflt_fnt,
                                           fg_color='#3a55eb', hover_color='#1a266b')
        self.browse_button.pack(side='left', padx=5)

        # Button to reset loaded img
        self.reset_btn = ctk.CTkButton(button_frame, text="Reset Image", command=self.reset_img, font=self.dflt_fnt,
                                       fg_color='#a62e2e', hover_color='#731f1f')
        self.reset_btn.pack(side='left', padx=5)

        # Null label to show the image
        self.image_label = ctk.CTkLabel(self.frame, text='No Image Selected')
        self.image_label.pack()

        # Segmented Button to choose the filter
        self.segButton = ctk.CTkSegmentedButton(self.frame, values=['Sobel', 'Prewitt', 'Roberts'],
                                                command=self.get_sgmntd_value, font=self.dflt_fnt)
        self.segButton.pack(pady=10, ipadx=100)

app1 = App1()
app1.mainloop()
