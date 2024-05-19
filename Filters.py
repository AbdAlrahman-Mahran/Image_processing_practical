import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import filedialog, IntVar, DoubleVar, StringVar
import cv2
import numpy as np

ctk.set_default_color_theme('green')


class App2(ctk.CTk):
    def __init__(self):
        super().__init__()
        self._set_appearance_mode('Dark')
        self.title('Filters')
        self.geometry('1024x720')
        self.frame = ctk.CTkScrollableFrame(self, fg_color='#171717')
        self.frame.pack(padx=5, pady=5, fill='both', expand=True)
        self.dflt_fnt = ctk.CTkFont(family='arial', weight='bold')
        self.original_img = None
        self.kernel_val = DoubleVar()
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
        img = ImageTk.PhotoImage(img)
        self.image_label.configure(image=img, text='')

    def reset_img(self):
        if self.original_img is not None:
            self.update_img(self.original_img)
            self.segButton.set(0)

    def get_sgmntd_value(self, value):
        if self.original_img is not None:
            if value == 'High-Pass':
                self.apply_hpf()
            elif value == 'Mean':
                self.apply_mean()
            elif value == 'Median':
                self.apply_median()
            elif value == 'Erosion':
                self.apply_erosion()
            elif value == "Dilation":
                self.apply_dilation()
            elif value == 'Open':
                self.apply_open()
            elif value == 'Close':
                self.apply_close()

        else:
            self.segButton.set(0)

    def apply_hpf(self):
        ksize = int(self.kernel_val.get())
        gray_img = cv2.cvtColor(self.original_img, cv2.COLOR_BGR2GRAY)
        gaussian_img = cv2.GaussianBlur(gray_img, (ksize, ksize), 0)
        hpf_img = cv2.subtract(gray_img, gaussian_img)
        self.update_img(cv2.cvtColor(hpf_img, cv2.COLOR_GRAY2BGR))

    def apply_mean(self):
        ksize = int(self.kernel_val.get())
        mean_img = cv2.blur(self.original_img, (ksize, ksize))
        self.update_img(mean_img)

    def apply_median(self):
        ksize = int(self.kernel_val.get())
        if ksize % 2 == 0:
            ksize += 1
        median_img = cv2.medianBlur(self.original_img, ksize)
        self.update_img(median_img)

    def apply_erosion(self):
        ksize = int(self.kernel_val.get())
        kernel = np.ones((ksize, ksize), np.uint8)
        eroised_img = cv2.erode(self.original_img, kernel, iterations=1)
        self.update_img(eroised_img)

    def apply_dilation(self):
        ksize = int(self.kernel_val.get())
        kernel = np.ones((ksize, ksize), np.uint8)
        dilation_img = cv2.dilate(self.original_img, kernel, iterations=1)
        self.update_img(dilation_img)

    def apply_open(self):
        ksize = int(self.kernel_val.get())
        kernel = np.ones((ksize, ksize), np.uint8)
        open_img = cv2.morphologyEx(self.original_img, cv2.MORPH_OPEN, kernel)
        self.update_img(open_img)

    def apply_close(self):
        ksize = int(self.kernel_val.get())
        kernel = np.ones((ksize, ksize), np.uint8)
        close_img = cv2.morphologyEx(self.original_img, cv2.MORPH_CLOSE, kernel)
        self.update_img(close_img)

    def add_buttons_sliders(self):
        # Frame to contain the buttons
        button_frame = ctk.CTkFrame(self.frame, fg_color='#171717')
        button_frame.pack(pady=10)

        # Button To Browse a photo
        self.browse_button = ctk.CTkButton(button_frame, text="Browse Image", command=self.load_img, font=self.dflt_fnt,
                                           fg_color='#3a55eb', hover_color='#1a266b')
        self.browse_button.pack(side='left', padx=5)

        # Button to reset loaded img
        self.reset_btn = ctk.CTkButton(button_frame, text="Reset Image", command=self.reset_img, font=(self.dflt_fnt),
                                       fg_color='#a62e2e', hover_color='#731f1f')
        self.reset_btn.pack(side='left', padx=5)

        # null label to show the image
        self.image_label = ctk.CTkLabel(self.frame, text='No Image Selected')
        self.image_label.pack()

        # Segmented Button to choose the filter
        self.segButton = ctk.CTkSegmentedButton(self.frame,
                                                values=['High-Pass', 'Mean', 'Median', 'Erosion', 'Dilation', 'Open',
                                                        'Close'], command=self.get_sgmntd_value, font=self.dflt_fnt)
        self.segButton.pack(pady=10, ipadx=100)

        # Slider to get kernel size
        self.ksize_slider_frame = ctk.CTkFrame(self.frame, corner_radius=8)
        self.ksize_slider_frame.pack()

        self.ksize_label = ctk.CTkLabel(self.ksize_slider_frame, text="Kernel Size: 1", font=self.dflt_fnt)
        self.ksize_label.pack()

        self.ksize_slider = ctk.CTkSlider(self.ksize_slider_frame, from_=1, to=20, number_of_steps=19, state='normal',
                                          command=self.update_ksize_label, variable=self.kernel_val)
        self.ksize_slider.set(0)
        self.ksize_slider.pack()

    def update_ksize_label(self, value):
        self.ksize_label.configure(text=f"Kernel Size: {int(value)}")
        self.get_sgmntd_value(self.segButton.get())


app1 = App2()
app1.mainloop()
