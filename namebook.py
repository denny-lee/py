#!/usr/bin/env python

# namebook
# by LW

from PyQt4 import QtCore, QtGui
from pymongo import MongoClient

WORD, TAG, HEAT = range(3)


class DbUtil():
    def __init__(self, ip, port):
        self.conn = MongoClient(ip, port)

    def save(self):



class WordBook():
    def __init__(self, word, tag):
        self.word = word
        self.tag = tag

    def save(self, conn):
        if not (self.word):
            # TODO  add hint.
            return



class Window(QtGui.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        # fileMenu = QtGui.QMenu("&File", self)
        # quitAction = fileMenu.addAction("E&xit")
        # quitAction.setShortcut("Ctrl+Q")
        # self.menuBar().addMenu(fileMenu)
        # quitAction.triggered.connect(self.close)

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
        # print(v1, v2)


def addCol(model, word, tag, heat):
    model.insertRow(0)
    model.setData(model.index(0, WORD), word)
    model.setData(model.index(0, TAG), tag)
    model.setData(model.index(0, HEAT), heat)


def createModel(parent):
    model = QtGui.QStandardItemModel(0, 3, parent)

    model.setHeaderData(WORD, QtCore.Qt.Horizontal, "Word")
    model.setHeaderData(TAG, QtCore.Qt.Horizontal, "Tag")
    model.setHeaderData(HEAT, QtCore.Qt.Horizontal, "Heat")

    addCol(model, "Happy New Year!", "Grace K. <grace@software-inc.com>",
            QtCore.QDateTime(QtCore.QDate(2006, 12, 31), QtCore.QTime(17, 3)))

    return model

if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.setModel(createModel(window))
    window.show()
    sys.exit(app.exec_())