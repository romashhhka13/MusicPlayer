"""Creating class for Buttons of Music Player"""

import tkinter as tk
import numpy as np

from tkinter import ttk


class Button(tk.Canvas):
    def __init__(self, master=None, width=None,
                 height=None, command=None,
                 type=None, scale=None,
                 highlightthickness=None,
                 background=None, highlightcolor=None,
                 highlightbackground=None):
        super().__init__(master=master, width=width,
                         height=height, background=background,
                         highlightthickness=highlightthickness,
                         highlightcolor=highlightcolor,
                         highlightbackground=highlightbackground,
                         cursor='hand2')

        self.width = width
        self.height = height
        self.scale = scale
        self.type = type
        self.fill_outline = highlightbackground
        self.width_outline = 1
        self.fill_item = highlightbackground
        self.fill_item_click = highlightbackground

        if self.type == 'pause':
            self.ButtonPause()
        elif self.type == 'play':
            self.ButtonPlayBack()
        elif self.type == 'next':
            self.ButtonNext()
        elif self.type == 'back':
            self.ButtonBack()


        self.bind('<Enter>', lambda event: self.configure(highlightthickness=1))
        self.bind('<Leave>', lambda event: self.configure(highlightthickness=0))
        # self.bind('<Button-1>', lambda event: self.config(bg='#E2CEE4'))
        # self.bind('<ButtonRelease-1>', lambda event: self.config(bg='#BEBEBE'))

        self.bind('<Enter>', lambda event: self.itemconfigure(self.type, fill=self.fill_item), add="+")
        self.bind('<Leave>', lambda event: self.itemconfigure(self.type, fill=self.fill_item), add="+")
        self.bind('<ButtonRelease-1>', lambda event: self.itemconfigure(self.type, fill=self.fill_item), add="+")

        if command is not None:
            self.bind('<Button-1>', command, add="+")
            self.bind('<Button-1>', lambda event: self.itemconfigure(self.type, fill=self.fill_item_click), add="+")

    # def place(self, x=None, y=None, relx=None, rely=None):
    #     self.object.place(x=x, y=y, relx=relx, rely=rely)

    def changeStatus(self, type=None):
        self.type = type
        if self.type == "pause":
            self.ButtonPause()
        elif self.type == 'play':
            self.ButtonPlayBack()

    def ButtonPlayBack(self):
        self.delete('all')
        x_center = self.width * 0.5
        y_center = self.width * 0.5
        x_left = x_center - self.width * self.scale * 0.44
        x_right = x_center + self.width * self.scale * 0.44
        y_top = y_center - self.height * self.scale * 0.5
        y_bottom = y_center + self.height * self.scale * 0.5

        rectangle1 = self.create_rectangle((x_left, y_top),
                                              (x_left + 1/3.2 * self.width * self.scale, y_bottom),
                                              tags=self.type)

        rectangle2 = self.create_rectangle((x_right - 1/3.2 * self.width * self.scale, y_top),
                                                  (x_right, y_bottom),
                                                  tags=self.type)

        self.itemconfigure(self.type, fill=self.fill_item, outline=self.fill_outline, width=self.width_outline)

    def ButtonPause(self):
        self.delete('all')
        x_center = self.width * 0.5
        y_center = self.width * 0.5
        x_left = x_center - ((self.width * self.scale) / 3)
        x_right = x_center + ((self.width * self.scale * 2) / 3)
        y_top = y_center - (x_center - x_left) / np.tan(np.pi / 6)
        y_bottom = y_center + (x_center - x_left) / np.tan(np.pi / 6)
        coordinate1 = [x_left, y_top]
        coordinate2 = [x_left, y_bottom]
        coordinate3 = [x_right, y_center]

        ButtonPlayBack = self.create_polygon(coordinate1,
                                                    coordinate2,
                                                    coordinate3,
                                                    tags=self.type)

        self.move(ButtonPlayBack, -1 / 9 * self.scale * self.width, 0)

        self.itemconfigure(self.type, fill=self.fill_item, outline=self.fill_outline, width=self.width_outline)

    def ButtonNext(self):
        self.delete('all')
        x_center = self.width * 0.5
        y_center = self.width * 0.5
        x_left = x_center - ((self.width * self.scale) / 3)
        x_right = x_center + ((self.width * self.scale * 2) / 3)
        y_top = y_center - (x_center - x_left) / np.tan(np.pi / 6)
        y_bottom = y_center + (x_center - x_left) / np.tan(np.pi / 6)
        coordinate1 = [x_left, y_top]
        coordinate2 = [x_left, y_bottom]
        coordinate3 = [x_right, y_center]

        ButtonPlayBack = self.create_polygon(coordinate1,
                                                    coordinate2,
                                                    coordinate3,
                                                    tags=self.type)

        Rectangle = self.create_rectangle((x_right*1.06, y_top),
                                                 ((x_right*1.14, y_bottom)),
                                                 tags=self.type)

        self.move(ButtonPlayBack, -1 / 5 * self.scale * self.width, 0)
        self.move(Rectangle, -1 / 5 * self.scale * self.width, 0)

        self.itemconfigure(self.type, fill=self.fill_item, outline=self.fill_outline, width=self.width_outline)

    def ButtonBack(self):
        self.delete('all')
        x_center = self.width * 0.5
        y_center = self.width * 0.5
        x_right = x_center + ((self.width * self.scale) / 3)
        x_left = x_center - ((self.width * self.scale * 2) / 3)
        y_top = y_center - (x_center - x_right) / np.tan(np.pi / 6)
        y_bottom = y_center + (x_center - x_right) / np.tan(np.pi / 6)
        coordinate1 = [x_right, y_top]
        coordinate2 = [x_right, y_bottom]
        coordinate3 = [x_left, y_center]

        ButtonPlayBack = self.create_polygon(coordinate1,
                                                    coordinate2,
                                                    coordinate3,
                                                    tags=self.type)

        Rectangle = self.create_rectangle((x_left*0.86, y_top),
                                                 ((x_left*0.7, y_bottom)),
                                                 tags=self.type)

        self.move(ButtonPlayBack, 1 / 5 * self.scale * self.width, 0)
        self.move(Rectangle, 1 / 5 * self.scale * self.width, 0)

        self.itemconfigure(self.type, fill=self.fill_item, outline=self.fill_outline, width=self.width_outline)


if __name__ == "__main__":
    a = (85 * 0.95 + 90 * 0.7 + 88 * 0.8) * 0.7
    b = (90 * 0.95 + 80 * 0.7 + 70 * 0.8) * 0.8
    c = (90 * 0.95 + 85 * 0.7 + 90 * 0.8) * 0.9
    d = (80 * 0.95 + 82 * 0.7 + 86 * 0.8) * 0.5
    print(a)
    print(b)
    print(c)
    print(d)
    print((a + b + c + d)/4)
    print((89*0.9 + 90*0.8 + 80*0.8) * 0.85 + (91 * 0.9 +87 * 0.8 +79 * 0.8) * 0.75 + (80*0.9+78*0.8+76*0.8) * 0.8)
