# -*- coding: utf-8 -*-
"""
Created on Mon Nov 06 12:29:11 2017

@author: User
"""

import shlex
import subprocess
from PIL import Image, ImageTk
import Tkinter as tk

#
#def run(text,strs):
#    while True:
#        text.set(strs)
#        text.update()

if __name__ == '__main__':
    root = tk.Tk()
    root.title('test window')
    root.geometry('500x550')
    label = tk.Label(root)
    t = tk.Text(label,bg='yellow',fg='black',width=300,height=65,font=('Arial',30))
    t.pack()
#    label.update()
    label.place(x=70,y=10,height=70,width=320)
    image = Image.open(r'C:\\Users\\User\\Desktop\\kth.png')
    bm = ImageTk.PhotoImage(image,height=400,width=460)
    label2 = tk.Label(root,image=bm,height=420,width=480)
    label2.place(x=10,y=100)
    root.update_idletasks()
    shell_cmd = 'python sub1.py'
    shell_cmd2 = 'python sub2.py'
    cmd1 = shlex.split(shell_cmd)
    cmd2 = shlex.split(shell_cmd2)
    p1 = subprocess.Popen(cmd1,shell=False)
    p2 = subprocess.Popen(cmd2,shell=False,stdout = subprocess.PIPE,stderr = subprocess.STDOUT)
    
    while p2.poll is not None:
        line = p2.stdout.readline()
        line = line.strip()
        if line:
            t.delete(1.0,tk.END)
            arr = line.split('&')
            if len(arr) == 2:
                try:
                    newImg = Image.open(arr[1])
                    newBm = ImageTk.PhotoImage(newImg)
                    label2.configure(image=newBm)
                except:
                    continue
                t.insert(tk.END,arr[0])
            else:
                label2.configure(image=bm)
            t.see(tk.END)
            t.update()
    root.mainloop()