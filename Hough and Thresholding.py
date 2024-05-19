import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import filedialog, DoubleVar
import cv2
import numpy as np

ctk.set_default_color_theme('green')


class App1(ctk.CTk):
    def __init__(self):
        super().__init__()
        self._set_appearance_mode('Dark')
        self.title('Hough and Tresholding')
        self.geometry('1024x720')
        self.frame = ctk.CTkScrollableFrame(self, fg_color='#171717')
        self.frame.pack(padx=5, pady=5, fill='both', expand=True)
        self.dflt_fnt = ctk.CTkFont(family='arial', weight='bold')
        self.original_img = None
        self.flag = False
        self.threshold_value = DoubleVar()
        self.processed_img_window = None
        self.add_buttons()

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
            if value == 'Hough-Circle':
                self.remove_slider()
                self.apply_hough()
            elif value == 'Threshold-Segmentation':
                if not self.flag:
                    self.add_slider()
                self.apply_thresholding()
        else:
            self.segButton.set(0)

    def apply_hough(self):
        gray_img = cv2.cvtColor(self.original_img, cv2.COLOR_BGR2GRAY)
        gray_img = cv2.medianBlur(gray_img, 5)
        img = cv2.cvtColor(gray_img, cv2.COLOR_GRAY2BGR)

        circles = cv2.HoughCircles(gray_img, cv2.HOUGH_GRADIENT, 1, 50, param1=50, param2=30, minRadius=23,
                                   maxRadius=41)
        circles = np.uint16(np.around(circles))
        if circles is not None:
            for circle in circles[0, :]:
                cv2.circle(img, (circle[0], circle[1]), circle[2], (0, 255, 0), 2)
                cv2.circle(img, (circle[0], circle[1]), 2, (0, 0, 255), 3)
        self.show_processed_img(img)

    def apply_thresholding(self):
        threshold_value = int(self.threshold_value.get())
        gray_img = cv2.cvtColor(self.original_img, cv2.COLOR_BGR2GRAY)
        _, threshold_img = cv2.threshold(gray_img, threshold_value, 255, cv2.THRESH_BINARY)
        self.show_processed_img(cv2.cvtColor(threshold_img, cv2.COLOR_GRAY2BGR))

    def show_processed_img(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        fin_img = ctk.CTkImage(dark_image=img, size=img.size)
        w,h = img.size

        if self.processed_img_window is None or not self.processed_img_window.winfo_exists():
            self.processed_img_window = ctk.CTkToplevel(self)
            self.processed_img_window.title('Processed Image')
            self.processed_img_window.geometry(f"{str(w)}x{str(h)}")
            self.processed_image_label = ctk.CTkLabel(self.processed_img_window, text='')
            self.processed_image_label.pack(expand=True)

        self.processed_image_label.configure(image=fin_img, text='')

    def add_buttons(self):
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
        self.segButton = ctk.CTkSegmentedButton(self.frame, values=['Hough-Circle', 'Threshold-Segmentation'],
                                                command=self.get_sgmntd_value, font=self.dflt_fnt)
        self.segButton.pack(pady=10, ipadx=100)

    def add_slider(self):
        self.tvalue_slider_frame = ctk.CTkFrame(self.frame)
        self.tvalue_slider_frame.pack()

        self.tvalue_label = ctk.CTkLabel(self.tvalue_slider_frame, text="Threshold Value: 127", font=self.dflt_fnt)
        self.tvalue_label.pack()

        self.tvalue_slider = ctk.CTkSlider(self.tvalue_slider_frame, from_=0, to=255, number_of_steps=255,
                                           state='normal', command=self.update_threshold_value,
                                           variable=self.threshold_value)
        self.tvalue_slider.set(127)
        self.tvalue_slider.pack()
        self.flag = True

    def remove_slider(self):
        if self.flag:
            self.tvalue_slider_frame.destroy()
            self.flag = False

    def update_threshold_value(self, value):
        self.tvalue_label.configure(text=f"Threshold Value: {int(value)}")
        self.get_sgmntd_value(self.segButton.get())


app1 = App1()
app1.mainloop()
