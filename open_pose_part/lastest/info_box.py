# -*- coding: utf-8 -*-

# author:Lichang

from Tkinter import *
tk = Tk()
flag = True
text = 'Hot posture captured' if flag else 'Cold posture captured'
label = Label(tk,text=text)
# button = Button(tk,text="Click me")
label.pack()
# button.pack()
tk.mainloop()

#
# def processOK():
#     print("OK button is clicked")
#
#
# def processCancel():
#     print("Cancel button is clicked")
#
#
# def main():
#     tk = Tk()
#     btnOK = Button(tk, text="OK", fg="red",
#                    command=processOK)
#     btnCancel = Button(tk, text="Cancel", fg="yellow",
#                        command=processCancel)
#     btnOK.pack()
#     btnCancel.pack()
#
#     tk.mainloop()
#
#
# if __name__ == '__main__':
#     main()
#
