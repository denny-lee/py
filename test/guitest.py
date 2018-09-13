#!/usr/bin/env python
# _*_ coding: utf-8
from tkinter import *

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master, width=200, height=200)
        self.pack()
        self.url = StringVar()
        self.method = StringVar()
        self.createWidgets()

    def createWidgets(self):
        self.title = Label(self, text='Fake Postman')
        self.title['background'] = 'red'
        self.title.grid(column=0,row=0)
        self.urlLabel = Label(self, text='Method:')
        self.urlLabel.grid(column=0,row=1)
        self.urlInput = Entry(self, textvariable=self.url)
        self.urlInput.grid(column=1,row=1)
        self.methodLabel = Label(self, text='Url:')
        self.methodInput = Entry(self, textvariable=self.method)
        self.method.set('GET')
        self.area = Text(self, width=40, height=10)
        self.area.grid(column=1,row=2)

        self.fireBtn = Button(self, text='Go', command=self.doit)
        self.fireBtn.grid(column=0,row=3,sticky='e')


    def doit(self):
        print(self.area.get(1.0, END))
        # self.quit()

app = Application()
# 设置窗口标题:
app.master.title('Hello World')
# 主消息循环:
app.mainloop()