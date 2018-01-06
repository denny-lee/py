#!/usr/bin/env python
# _*_ coding: utf-8
from tkinter import *

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.e = StringVar()
        self.createWidgets()

    def createWidgets(self):
        self.helloLabel = Label(self, text='Hello, world!')
        self.helloLabel.pack()
        self.quitButton = Button(self, text='Quit', command=self.doit)
        self.quitButton.pack()
        self.enter = Entry(self, textvariable=self.e)
        # self.e.set("abc")
        self.enter.pack()

    def doit(self):
        print(self.e.get())
        self.quit()

app = Application()
# 设置窗口标题:
app.master.title('Hello World')
# 主消息循环:
app.mainloop()

