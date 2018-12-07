#!/usr/bin/env python
# _*_ coding: utf-8
from tkinter import *
from tkinter import ttk
import http.client as client
from tkinter import font

class Application(ttk.Panedwindow):
    def __init__(self, master=None):
        # self.mainTitleFont = font.Font(family='Helvetica', size=18, weight='bold')
        pw=ttk.Panedwindow.__init__(self, master, orient=VERTICAL, width=800)
        self.pack()
        self.f0 = ttk.Labelframe(self, text='')
        self.f1 = ttk.Labelframe(self, text='Request')
        self.f2 = ttk.Notebook(self.f1)
        self.f3 = ttk.Labelframe(self, text='Response')
        self.f1.grid_rowconfigure(0, weight=1)
        self.f3.grid_rowconfigure(0, weight=1)
        self.f1.grid_columnconfigure(0, weight=1)
        self.f3.grid_columnconfigure(0, weight=1)
        self.add(self.f0)
        self.add(self.f1)
        # self.add(self.f2)
        self.add(self.f3)
        self.url = StringVar()
        self.method = StringVar()
        self.netType = StringVar()
        self.respStatus = StringVar()
        self.dataType = StringVar()
        self.respContent = None
        self.reqHeader = None
        self.reqBody = None
        self.statusBar = None

        self.createWidgets()

    def createWidgets(self):
        Label(self.f0, text='Post Girl', font=font.Font(size=14, weight='bold')).pack()

        Label(self.f1, text='Method:').grid(column=0, row=0)
        cbb = ttk.Combobox(self.f1, textvariable=self.method, width=15)
        cbb.grid(column=1, row=0, sticky="w")
        cbb['values'] = ('GET', 'POST', 'PUT', 'DELETE')
        cbb.bind('<<ComboboxSelected>>', self.onchange)
        self.method.set('POST')
        Radiobutton(self.f1, text='Inner', width=20, foreground='gray', font=font.Font(weight='bold'), variable=self.netType, value='Inner').grid(column=2,row=0)
        Radiobutton(self.f1, text='Outer', width=20, foreground='blue', font=font.Font(weight='bold'), variable=self.netType, value='Outer').grid(column=3,row=0)
        self.netType.set('Inner')

        Label(self.f1, text='Url:').grid(column=0, row=1)
        Entry(self.f1, textvariable=self.url, width=80).grid(column=1, row=1, columnspan=3, sticky="w")
        self.url.set('localhost:8080/biz')

        Button(self.f1, text='Go', foreground='green', width=8, font=font.Font(size=18, weight='bold'), command=self.doit).grid(column=4,row=0,rowspan=2, sticky=(N, S, W, E))

        # Child Frame for request params
        nHeader = Frame(self.f2)
        nBody = Frame(self.f2)
        self.f2.add(nHeader, text='Headers')
        self.f2.add(nBody, text='Body')
        self.reqHeader = Text(nHeader, width=95, height=10)
        self.reqHeader.grid(column=0, row=0, columnspan=3)

        self.reqBody = Text(nBody, width=95, height=10)
        Radiobutton(nBody, text='text', variable=self.dataType, value='text', command=self.toggle).grid(column=0, row=0)
        Radiobutton(nBody, text='json', variable=self.dataType, value='json', command=self.toggle).grid(column=1, row=0)
        Radiobutton(nBody, text='xml', variable=self.dataType, value='xml', command=self.toggle).grid(column=2, row=0)
        Radiobutton(nBody, text='form', variable=self.dataType, value='form', command=self.toggle).grid(column=3, row=0)
        self.dataType.set('json')
        self.reqBody.grid(column=0, row=1, columnspan=4)
        sbar1 = Scrollbar(nBody,orient=VERTICAL, command=self.reqBody.yview)
        sbar1.grid(column=4, row=1,sticky=(N,S))
        self.reqBody.config(yscrollcommand=sbar1.set)
        self.reqBody.insert(END, '{}')
        self.f2.grid(column=0, row=2, columnspan=5)


        # Child Frame for response.
        self.statusBar = Label(self.f3, text='    ')
        self.statusBar.grid(column=0, row=0)
        Label(self.f3, text='Status:').grid(column=1, row=0)
        Entry(self.f3, textvariable=self.respStatus).grid(column=2, row=0)
        self.respContent = Text(self.f3, width=95, height=10)
        self.respContent.grid(column=0, row=1, columnspan=3)
        sbar2 = Scrollbar(self.f3, orient=VERTICAL, command=self.respContent.yview)
        sbar2.grid(column=3, row=1, sticky=(N, S))
        self.respContent.config(yscrollcommand=sbar2.set)

    def onchange(self, event):
        pass

    def toggle(self):
        dataType = self.dataType.get()
        if dataType == 'json':
            self.reqBody.delete(1.0, END)
            self.reqBody.insert(END, '{}')
        elif dataType == 'form':
            self.reqBody.delete(1.0, END)
            pass
        else:
            self.reqBody.delete(1.0, END)
            pass

    def parseUrl(self):
        if '://' in self.url.get():
            url = self.url.get().split('://')[1]
        else:
            url = self.url.get()

        if '/' not in url:
            targetPage = '/'
            domain = url
        else:
            idx = url.index('/')
            (domain, targetPage) = (url[:idx], url[idx:])
        return domain, targetPage

    def parseHeader(self):
        text = self.reqHeader.get(1.0, END)
        if '\r\n' in text:
            hArr = text.split('\r\n')
        elif '\n' in text:
            hArr = text.split('\n')
        elif len(text) > 0:
            hArr = [text]
        else:
            hArr = []

        headers = {}
        for str in hArr:
            if ':' in str:
                idx = str.index(':')
                headers[str[:idx]] = str[idx+1:].strip()

        dataType = self.dataType.get()
        if not headers.get('Content-Type') and not headers.get('Content-type') and not headers.get('content-type'):
            if dataType == 'json':
                headers['Content-Type'] = 'application/json;charset=UTF-8'
            elif dataType == 'xml':
                headers['Content-Type'] = 'application/xml;charset=UTF-8'
            elif dataType == 'form':
                headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF-8'
            else:
                headers['Content-Type'] = 'application/text;charset=UTF-8'

        if self.reqBody.get(1.0, END):
            headers['Content-Length'] = len(self.reqBody.get(1.0, END))
        return headers

    def doit(self):
        self.respContent.delete(1.0, END)
        (domain, targetPage) = self.parseUrl()
        method = self.method.get()
        netType = self.netType.get()

        headers = self.parseHeader()

        # print(url, domain, targetPage)
        if self.reqBody.get(1.0, END):
            reqBody = self.reqBody.get(1.0, END)
        else:
            reqBody = None

        if netType == 'Inner':
            conn = client.HTTPConnection(domain)
            conn.request(method, targetPage, headers=headers, body=reqBody)
        elif netType == 'Outer':
            headers["Host"] = domain
            conn = client.HTTPConnection("10.248.192.245:80")
            conn.request(method, targetPage, headers=headers, body=reqBody)
        else:
            raise Exception('Wrong parameters!')

        data = conn.getresponse()
        self.respStatus.set(data.status)
        if 200 == data.status:
            self.statusBar['background'] = 'green'
        else:
            self.statusBar['background'] = 'red'
        self.respContent.insert(END, data.read())
        conn.close()

app = Application()
# 设置窗口标题:
app.master.title('Post Girl')
# 主消息循环:
app.mainloop()