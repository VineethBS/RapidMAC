# ! /usr/bin/env python 3.6.7
# -*- coding utf-8 -*-

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets
from node_editor_wnd import NodeEditorWnd
from node_node import codefragmenttext, St_node, Wp_node, Rb_node, Sp_node
from node_edge import codefragment

listItems = ["Start Node","Wait for Packet","Random Backoff","Send Packet"]
#LIST_FLAG = 0

class MainWin(QMainWindow):
    def __init__(self):
        print('*----nodeEditor_main----*')  
        super(MainWin,self).__init__()
        self.list_flag = [0]    # for the ease of passing value
        self.start = " "
        self.end = " "
        toolbar = self.addToolBar('Toolbar')
        btn1 = QPushButton('Nodes', self)
        btn2 = QPushButton('Edges', self)
        btn3 = QPushButton('Select', self)
        btn4 = QPushButton('Save File', self)   # for saving codefragment
        toolbar.addWidget(btn1)
        toolbar.addWidget(btn2)
        toolbar.addWidget(btn3)
        toolbar.addWidget(btn4)         # for Save File button

        btn4.clicked.connect(self.savebuttonClicked)    # signal to slot

        self.list = QListWidget()
        for i in range (4): self.list.addItem(listItems[i])
        self.list.clicked.connect(self.listbox_clicked)    # signal to slot
       
        left = NodeEditorWnd(self,self.list_flag)   # passing the value as a list

        splitter1 = QSplitter(Qt.Horizontal)
        splitter1.addWidget(left)
        splitter1.addWidget(self.list)
        splitter1.setSizes([300,50])
        
        self.statusBar().showMessage('Ready')
        self.showMaximized()
        self.setCentralWidget(splitter1)    # **very important
        self.setWindowTitle('Rapid MAC')
        self.show()
 
    def savebuttonClicked(self):
        with open('codefragment.py','w') as myfile:
            for k in codefragment:
                print(k, ' ', codefragment[k])
                print(St_node)
                print(Wp_node)
                if k in St_node:
                    myfile.write(str("Start Node"))
                if k in Wp_node:
                    myfile.write("Wait for Packet Node")
                if k in Rb_node:
                    myfile.write("Random Backoff Node")
                if k in Sp_node: 
                    myfile.write("Send Packet Node")
##                myfile.write(Start)
                myfile.write(' ----> ')
                if codefragment[k] in St_node:
                    myfile.write("Start Node")
                if codefragment[k] in Wp_node:
                    myfile.write("Wait for Packet Node")
                if codefragment[k] in Rb_node:
                    myfile.write("Random Backoff Node")
                if codefragment[k] in Sp_node: 
                    myfile.write("Send Packet Node")
##                myfile.write(End)
                myfile.write('\n')
##                print("self.start = ",self.start)
##                print("self.end = ", self.end)
##                myfile.write("%s" % self.start)
##                myfile.write(' to ')
##                myfile.write("%s\n" % self.end)
##                myfile.write('\n')
##        with open('codefragment.py','w') as myfile:
##            myfile.write(str(codefragment))
##            for key,val in codefragment:
##              myfile.write("%s\n" % codefragment[key])

    def listbox_clicked(self):
#        global LIST_FLAG
        item = self.list.currentItem()
        print(str(item.text()))
        if str(item.text()) == listItems[0]:
            self.list_flag[0] = 1
            self.statusBar().showMessage(listItems[0])
        if str(item.text()) == listItems[1]:
            self.list_flag[0] = 2
            self.statusBar().showMessage(listItems[1])
        if str(item.text()) == listItems[2]:
            self.list_flag[0] = 3
            self.statusBar().showMessage(listItems[2])
        if str(item.text()) == listItems[3]:
            self.list_flag[0] = 4
            self.statusBar().showMessage(listItems[3])
        print("clicked item:", self.list_flag)  


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWin()
    sys.exit(app.exec_())
    

