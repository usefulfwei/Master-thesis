# -*- coding: utf-8 -*-

# author:Lichang

from tkinter import *
import os

class App:
    def __init__(self, master):
        self.frame = Frame(master)
        self.b = Button(self.frame, text='Open', command=self.openFile)
        self.c = Button(self.frame, text='Open', command=self.openFile)
        self.b.grid(row=1,column=0)
        self.c.grid(row=1,column=4)
        self.frame.grid()

    def openFile(self):
        os.startfile(r'C:\Program Files (x86)\Noël Danjou\AMCap\amcap.exe')

root = Tk()
root.title('my window')
root.geometry('200x100')

app = App(root)
root.mainloop()