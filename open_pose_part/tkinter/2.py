# -*- coding: utf-8 -*-

# author:Lichang
import os
from tkinter import *
import multiprocessing as mp

def openpose_job():
    pass

def analysis_job():
    pass

class App:
    def __init__(self, master):
        self.frame = Frame(master,height=100,width=350)
        self.b = Button(self.frame, text='OpenCamera', command=self.openFile)
        self.c = Button(self.frame, text='OpenAnalysis', command=self.openProcess)
        self.var1 = StringVar()
        self.d = Button(self.frame, text='OpenUnderstanding', command=self.openAnalysis)
        self.e = Label(self.frame,textvariable=self.var1)
        self.b.grid(row=1, column=0)
        self.c.grid(row=1, column=1)
        self.d.grid(row=1, column=2)
        self.e.grid(row=1, column=3)
        self.frame.grid()

    def openFile(self):
        os.startfile(r'C:\Program Files (x86)\Noël Danjou\AMCap\amcap.exe')

    def openProcess(self):
        p = mp.Process(target=openpose_job)
        p.start()
        p.join()
    def openAnalysis(self,textEle):
        p = mp.Process(target=analysis_job,args=textEle)
        p.start()
        p.join()


if __name__ == '__main__':
    root = Tk()
    root.title('my window')
    root.geometry('500x100')

    # p1 = mp.Process(target=openpose_job)
    # p2 = mp.Process(target=analysis_job)
    app = App(root)
    # p1.start()
    # p2.start()
    # p1.join()
    # p2.join()
    root.mainloop()
