#!/usr/bin/env python

# namebook
# by LW

from PyQt4 import QtCore, QtGui
from pymongo import MongoClient

WORD, TAG, HEAT = range(3)
page_size = 10

class DbUtil():
    def __init__(self, ip='localhost', port=27017):
        self.ip = ip
        self.port = port
        self.conn = MongoClient(ip, port)

    def save(self, data):
        if not data:
            return
        if not self.conn:
            self.conn = MongoClient(self.ip, self.port)
        self.conn.learn.namebook.save(data)
    def findOne(self, data):
        if not data:
            return None
        return self.conn.learn.namebook.find_one(data)
    def page(self, pageNo, pageSize):
        skip = pageSize * (pageNo - 1)
        return self.conn.learn.namebook.find().skip(skip).limit(pageSize)
    def close(self):
        if (self.conn):
            self.conn.close()

class WordBook():
    def __init__(self, word, tag, db):
        self.word = word
        self.tag = tag
        self.db = db
        self.msg_box = QtGui.QMessageBox(QtGui.QMessageBox.Warning, "Alert", "Word must not null!")

    def save(self):
        if not (self.word):
            if not self.msg_box:
                self.msg_box = QtGui.QMessageBox(QtGui.QMessageBox.Warning, "Alert", "Word must not null!")
            self.msg_box.show()
            return
        data = self.db.findOne({'word':self.word})
        if not data:
            data = {}
            tag = self.tag
        else:
            tag = data['tag'] + ',' + self.tag
        data1 = {'word':self.word, 'tag':tag}
        data = {**data, **data1}
        self.db.save(data)


class Window(QtGui.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        # fileMenu = QtGui.QMenu("&File", self)
        # quitAction = fileMenu.addAction("E&xit")
        # quitAction.setShortcut("Ctrl+Q")
        # self.menuBar().addMenu(fileMenu)
        # quitAction.triggered.connect(self.close)

        self.ds = None

        self.listGroupBox = QtGui.QGroupBox("WordList")
        self.addGroupBox = QtGui.QGroupBox("Add")

        self.dataView = QtGui.QTreeView()
        self.dataView.setRootIsDecorated(False)
        self.dataView.setAlternatingRowColors(True)

        dataLayout = QtGui.QHBoxLayout()
        dataLayout.addWidget(self.dataView)
        self.listGroupBox.setLayout(dataLayout)

        self.wordEdit = QtGui.QLineEdit()
        self.wordLabel = QtGui.QLabel("&Word:")
        self.wordLabel.setBuddy(self.wordEdit)

        self.tagEdit = QtGui.QLineEdit()
        self.tagLabel = QtGui.QLabel("&Tag:")
        self.tagLabel.setBuddy(self.tagEdit)

        saveButton = QtGui.QPushButton("&Save")
        saveButton.clicked.connect(self.saveItem)

        addLayout = QtGui.QGridLayout()
        addLayout.addWidget(self.wordLabel, 0, 0)
        addLayout.addWidget(self.wordEdit, 0, 1, 1, 3)
        addLayout.addWidget(self.tagLabel, 1, 0)
        addLayout.addWidget(self.tagEdit, 1, 1, 1, 3)
        addLayout.addWidget(saveButton, 3, 3, 1, 1)
        self.addGroupBox.setLayout(addLayout)

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.addWidget(self.listGroupBox)
        mainLayout.addWidget(self.addGroupBox)
        self.setLayout(mainLayout)

        self.setWindowTitle("Name Book")
        self.resize(500, 450)

    def setModel(self, model):
        self.dataView.setModel(model)

    def saveItem(self):
        word = self.wordEdit.text()
        tag = self.tagEdit.text()
        ds = self.ds
        wordbook = WordBook(word, tag, ds)
        wordbook.save()

    def setDatabase(self, ds):
        self.ds = ds

    def closeEvent(self, event):
        self.ds.close()
        event.accept()


def addCol(model, word, tag, heat):
    model.insertRow(0)
    model.setData(model.index(0, WORD), word)
    model.setData(model.index(0, TAG), tag)
    model.setData(model.index(0, HEAT), heat)


def createModel(parent, ds):
    model = QtGui.QStandardItemModel(page_size, 3, parent)

    model.setHeaderData(WORD, QtCore.Qt.Horizontal, "Word")
    model.setHeaderData(TAG, QtCore.Qt.Horizontal, "Tag")
    model.setHeaderData(HEAT, QtCore.Qt.Horizontal, "Heat")

    list = ds.page(1, page_size)
    for workbook in list:
        addCol(model, workbook['word'], workbook['tag'], '')
    #           QtCore.QDateTime(QtCore.QDate(2006, 12, 31), QtCore.QTime(17, 3)))

    return model

if __name__ == '__main__':

    import sys

    ip = None
    port = None
    if len(sys.argv) == 3:
        ip = sys.argv[1]
        port = sys.argv[2]
    if len(sys.argv) == 2:
        ip = sys.argv[1]

    app = QtGui.QApplication(sys.argv)
    window = Window()
    ds = DbUtil(ip, port)
    window.setDatabase(ds)
    window.setModel(createModel(window, ds))
    window.show()
    sys.exit(app.exec_())