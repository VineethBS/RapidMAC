# ! /usr/bin/env python 3.6.7
# -*- coding utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets
from node_editor_wnd import NodeEditorWnd
from node_node import Node, codefragmenttext, St_Init_node,St_SP_node,St_PI_node,St_On_node,St_Off_node,St_CCI_node, Wp_node, Rb_node, Sp_node,Rv_node,Cust_node
from node_node import Start_Node_Init,Start_Node_SP,Start_Node_PI,Start_Node_On,Start_Node_Off,Start_Node_CCI
from node_node import Waitforpkt_Node,Randombackoff_Node,Sendpacket_Node,ReturnValue_Node,FunctionCall_Node,VariableAssign_Node
from node_edge import Edge, codefragment
from node_graphics_view import INIT_content,SP_content,PI_content,ON_content1,ON_content2,OFF_content1,OFF_content2,CCI_content1,CCI_content2
from node_graphics_view import Ret_textinputs,Custom_textinputs
import sys
import networkx as nx
import matplotlib.pyplot as plt
import pickle

mac_functions = ["init", "send_packet", "packet_input", "on", "off", "channel_check_interval"]
func_blocks = ["Wait for Packet","Random Backoff","Send Packet","Return Value","Function Call","Variable Assignment","Custom Code Block"]

Dict_db = {}


class MainWin(QMainWindow):
    def __init__(self):  
        super(MainWin,self).__init__()
        self.list_flag = [0]   
        self.net = nx.DiGraph()
        self.count = 0
        self.node_content = "RAPID MAC - Main Window"
        self.flag = 0
        codefragment_copy = codefragment.copy()

        self.On_Cust_txt = " "
        self.Off_Cust_txt = " "
        self.CCI_Cust_txt = " "
        self.On_Ret_txt = " "
        self.Off_Ret_txt = " "
        self.CCI_Ret_txt = " "
        
        toolbar = self.addToolBar('Toolbar')
        btn1 = QPushButton('Nodes', self)
        btn2 = QPushButton('Edges', self)
        btn3 = QPushButton('Select', self)
        btn4 = QPushButton('Save File', self)    
        toolbar.addWidget(btn1)
        toolbar.addWidget(btn2)
        toolbar.addWidget(btn3)
        toolbar.addWidget(btn4)         

        btn4.clicked.connect(self.savebuttonClicked)    

        listsplitter = QFrame()
##        frame_1 = QFrame()
##        frame_1.setFrameShape(QFrame.StyledPanel)
        label1 = QLabel()
        label1.setText('MAC Functions:')
        label1.setStyleSheet('font: 18px;')
##        frame_1.addWidget(label1)
        
##        frame_2 = QFrame()
##        frame_2.setFrameShape(QFrame.StyledPanel)
        label2 = QLabel()
        label2.setText('Functional Blocks:')
        label2.setStyleSheet('font: 18px;')
##        frame_2.addWidget(label2)

        self.list1 = QListWidget()
        for i in range (6): self.list1.addItem(mac_functions[i])
##        frame_1.addWidget(self.frame1)
        self.list1.clicked.connect(self.listbox1_clicked)
        
        self.list2 = QListWidget()
        for i in range (7): self.list2.addItem(func_blocks[i])
##        frame_2.addWidget(self.frame2)
        self.list2.clicked.connect(self.listbox2_clicked)    
       
        left = NodeEditorWnd(self,self.list_flag,self.net,self.node_content)    

##        listsplitter = QSplitter(Qt.Vertical)
        splitter1 = QSplitter(Qt.Horizontal)

        layout = QVBoxLayout()

        layout.addWidget(label1)
##        layout.addStretch()
        layout.addWidget(self.list1)
        layout.addWidget(label2)
##        layout.addStretch()
        layout.addWidget(self.list2)

        listsplitter.setLayout(layout)
        
        splitter1.addWidget(left)
        splitter1.addWidget(listsplitter)
        splitter1.setSizes([800,30])
        
        self.statusBar().showMessage('Ready')
        self.showMaximized()
        self.setCentralWidget(splitter1)     
        self.setWindowTitle('Rapid MAC')
        self.show()
 
    def listbox1_clicked(self):
        item = self.list1.currentItem()
        if str(item.text()) == mac_functions[0]:
            self.list_flag[0] = 1
            self.statusBar().showMessage(mac_functions[0])
        if str(item.text()) == mac_functions[1]:
            self.list_flag[0] = 2
            self.statusBar().showMessage(mac_functions[1])
        if str(item.text()) == mac_functions[2]:
            self.list_flag[0] = 3
            self.statusBar().showMessage(mac_functions[2])
        if str(item.text()) == mac_functions[3]:
            self.list_flag[0] = 4
            self.statusBar().showMessage(mac_functions[3])
        if str(item.text()) == mac_functions[4]:
            self.list_flag[0] = 5
            self.statusBar().showMessage(mac_functions[4])
        if str(item.text()) == mac_functions[5]:
            self.list_flag[0] = 6
            self.statusBar().showMessage(mac_functions[5])

    def listbox2_clicked(self):
        item = self.list2.currentItem()
        if str(item.text()) == func_blocks[0]:
            self.list_flag[0] = 7
            self.statusBar().showMessage(func_blocks[0])
        if str(item.text()) == func_blocks[1]:
            self.list_flag[0] = 8
            self.statusBar().showMessage(func_blocks[1])
        if str(item.text()) == func_blocks[2]:
            self.list_flag[0] = 9
            self.statusBar().showMessage(func_blocks[2])
        if str(item.text()) == func_blocks[3]:
            self.list_flag[0] = 10
            self.statusBar().showMessage(func_blocks[3])
        if str(item.text()) == func_blocks[4]:
            self.list_flag[0] = 11
            self.statusBar().showMessage(func_blocks[4])
        if str(item.text()) == func_blocks[5]:
            self.list_flag[0] = 12
            self.statusBar().showMessage(func_blocks[5])
        if str(item.text()) == func_blocks[6]:
            self.list_flag[0] = 13
            self.statusBar().showMessage(func_blocks[6])

    def savebuttonClicked(self):
        codefragment_copy = []
        Flow1 = []
        Flow2 = []
        Flow3 = []
        Flow4 = []
        Flow5 = []
        Flow6 = []

        print('Code Fragment:', codefragment)
        print('len(codefragment) = ',len(codefragment))
        print('St_Init_node:',St_Init_node)
        print('St_SP_node:',St_SP_node)
        print('St_PI_node:',St_PI_node)
        print('St_On_node:',St_On_node)
        print('St_Off_node:',St_Off_node)
        print('St_CCI_node:',St_CCI_node)
        print('Wp_node:',Wp_node)
        print('Rb_node:',Rb_node)
        print('Sp_node:',Sp_node)
        
        self.draw_nxgraph()
        
        # check if all the MAC Function nodes are created
        st1 = len(St_Init_node)
        st2 = len(St_SP_node)
        st3 = len(St_PI_node)
        st4 = len(St_On_node)
        st5 = len(St_Off_node)
        st6 = len(St_CCI_node)

        for i in range (len(codefragment)):
            codefragment_copy.append(codefragment[i])
            
        print('Codefragment_copy = ',codefragment_copy)

        for i in range (len(codefragment_copy)):
            print("codefragment_copy = ",codefragment_copy)
            print("i = ",i)
            k = codefragment_copy[0]
            print (k)
       
            if k[0] in St_SP_node:
                Flow2.append(k)
                codefragment_copy.remove(k)
                for j in range (len(codefragment_copy)):
                    k1 = codefragment_copy[j]
                    if k1[0] == k[1]:
                        Flow2.append(k1)
                        codefragment_copy.remove(k1)
                        for m in range (len(codefragment_copy)):
                            k2 = codefragment_copy[m]
                            if k2[0] == k1[1]:
                                Flow2.append(k2)
                                codefragment_copy.remove(k2)
                                break
                        break
            if k[0] in St_PI_node:
                Flow3.append(k)
                codefragment_copy.remove(k)
                for j in range (len(codefragment_copy)):
                    k1 = codefragment_copy[j]
                    if k1[0] == k[1]:
                        Flow3.append(k1)
                        codefragment_copy.remove(k1)
                        for m in range (len(codefragment_copy)):
                            k2 = codefragment_copy[m]
                            if k2[0] == k1[1]:
                                Flow3.append(k2)
                                codefragment_copy.remove(k2)
                                break
                        break
            if k[0] in St_On_node:
                Flow4.append(k)           
                codefragment_copy.remove(k)
                for j in range (len(codefragment_copy)):
                    k1 = codefragment_copy[j]
                    if k1[0] == k[1]:
                        Flow4.append(k1)
                        codefragment_copy.remove(k1)
                        for m in range (len(codefragment_copy)):
                            k2 = codefragment_copy[m]
                            if k2[0] == k1[1]:
                                Flow4.append(k2)
                                codefragment_copy.remove(k2)
##                                for n in range (len(codefragment_copy)):
##                                    k3 = codefragment_copy[n]
##                                    if k3[0] == k2[1]:
##                                        Flow4.append(k3)
##                                        codefragment_copy.remove(k3)
##                                        break
                                break
                        break
            if k[0] in St_Off_node:
                Flow5.append(k)
                codefragment_copy.remove(k)
                for j in range (len(codefragment_copy)):
                    k1 = codefragment_copy[j]
                    if k1[0] == k[1]:
                        Flow5.append(k1)
                        codefragment_copy.remove(k1)
                        for m in range (len(codefragment_copy)):
                            k2 = codefragment_copy[m]
                            if k2[0] == k1[1]:
                                Flow5.append(k2)
                                codefragment_copy.remove(k2)
##                                for n in range (len(codefragment_copy)):
##                                    k3 = codefragment_copy[n]
##                                    if k3[0] == k2[1]:
##                                        Flow5.append(k3)
##                                        codefragment_copy.remove(k3)
##                                        break
                                break
                        break
            if k[0] in St_CCI_node:
                Flow6.append(k)
                codefragment_copy.remove(k)
                for j in range (len(codefragment_copy)):
                    k1 = codefragment_copy[j]
                    if k1[0] == k[1]:
                        Flow6.append(k1)
                        codefragment_copy.remove(k1)
                        for m in range (len(codefragment_copy)):
                            k2 = codefragment_copy[m]
                            if k2[0] == k1[1]:
                                Flow6.append(k2)
                                codefragment_copy.remove(k2)
##                                for n in range (len(codefragment_copy)):
##                                    k3 = codefragment_copy[n]
##                                    if k3[0] == k2[1]:
##                                        Flow6.append(k3)
##                                        codefragment_copy.remove(k3)
##                                        break
                                break
                        break
            if (len(codefragment_copy)) != 0:
                continue
            else:
                break

        print("Flow1 = ",Flow1)
        print("Flow2 = ",Flow2)
        print("Flow3 = ",Flow3)
        print("Flow4 = ",Flow4)
        print("Flow5 = ",Flow5)
        print("Flow6 = ",Flow6)
        print("Custom_textinputs:",Custom_textinputs)
        
        if st1 == 1 and st2 == 1 and st3 == 1 and st4 == 1 and st5 == 1 and st6 == 1:
            with open ('codefragment.c','w') as self.myfile:
                self.myfile.write("\n")
                self.myfile.write(INIT_content)
                self.myfile.write("\n/*---------------------------------------------------------------------------------*/\n")
                self.myfile.write("\n")
                self.myfile.write(SP_content)
                self.myfile.write("\n/*---------------------------------------------------------------------------------*/\n")
                self.myfile.write("\n")
                self.myfile.write(PI_content)
                self.myfile.write("\n/*---------------------------------------------------------------------------------*/\n")
                
                
                for s in range (len(Flow4)):
                    w = Flow4[s]
                    for s1 in range (len(Custom_textinputs)):
                        w1 = Custom_textinputs[s1]
                        if w1[0] == w[1]:
                            self.On_Cust_txt = w1[1]
                            print("=====",self.On_Cust_txt,"=====")
##                            break
                    for t in range (len(Ret_textinputs)):
                        x = Ret_textinputs[t]
        ##                                print('Flow4;x[1] = ',x[1])
                        if x[0] == w[1]:
                            print('x[0] = ',x[0],'k[1] = ',w[1])
                            self.On_Ret_txt = x[1]
                            print("==== self.On_Ret_txt: ",self.On_Ret_txt,"====")
##                            break
                if self.On_Cust_txt is None:
                    self.On_Cust_txt = " "
                if self.On_Ret_txt is None:
                    self.On_Ret_txt = " "
                self.myfile.write("\n")
                self.myfile.write(ON_content1 + self.On_Cust_txt + self.On_Ret_txt + ON_content2)
                self.myfile.write("\n/*---------------------------------------------------------------------------------*/\n")
                

                for s in range (len(Flow5)):
                    w = Flow5[s]
                    for s1 in range (len(Custom_textinputs)):
                        w1 = Custom_textinputs[s1]
                        if w1[0] == w[1]:
                            self.Off_Cust_txt = w1[1]
                            print("=====",self.Off_Cust_txt,"=====")
                    for t in range (len(Ret_textinputs)):
                        x = Ret_textinputs[t]
                        if x[0] == w[1]:
                            self.Off_Ret_txt = x[1]
                            print("====",self.Off_Ret_txt,"====")

                if self.Off_Cust_txt is None:
                    self.Off_Cust_txt = " "
                if self.Off_Ret_txt is None:
                    self.Off_Ret_txt = " "
                self.myfile.write("\n")
                self.myfile.write(OFF_content1 + self.Off_Cust_txt + self.Off_Ret_txt + OFF_content2)
                self.myfile.write("\n/*---------------------------------------------------------------------------------*/\n")
               
                
                for s in range (len(Flow6)):
                    w = Flow6[s]
                    for s1 in range (len(Custom_textinputs)):
                        w1 = Custom_textinputs[s1]
                        if w1[0] == w[1]:
                            self.CCI_Cust_txt = w1[1]
                            print("=====",self.CCI_Cust_txt,"=====")
                    for t in range (len(Ret_textinputs)):
                        x = Ret_textinputs[t]
                        if x[0] == w[1]:
                            self.CCI_Ret_txt = x[1]
                            print("====",self.CCI_Ret_txt,"====")

                if self.CCI_Cust_txt is None:
                    self.CCI_Cust_txt = " "
                if self.CCI_Ret_txt is None:
                    self.CCI_Ret_txt = " "
                self.myfile.write("\n")
                self.myfile.write(CCI_content1 + self.CCI_Cust_txt + self.CCI_Ret_txt + CCI_content2)
                self.myfile.write("\n/*---------------------------------------------------------------------------------*/\n")
                
                for a in range (len(Flow2)):
                    A = Flow2[a]
##                    print("a = ",a, 'A = ',A)
                    self.node1 = A[0]
                    self.node2 = A[1]
                    self.writefile()
                for a in range (len(Flow3)):
                    A = Flow3[a]
##                    print("a = ",a, 'A = ',A)
                    self.node1 = A[0]
                    self.node2 = A[1]
                    self.writefile()
                for a in range (len(Flow4)):
                    A = Flow4[a]
##                    print("a = ",a, 'A = ',A)
                    self.node1 = A[0]
                    self.node2 = A[1]
                    self.writefile()
                for a in range (len(Flow5)):
                    A = Flow5[a]
##                    print("a = ",a, 'A = ',A)
                    self.node1 = A[0]
                    self.node2 = A[1]
                    self.writefile()
                for a in range (len(Flow6)):
                    A = Flow6[a]
##                    print("a = ",a, 'A = ',A)
                    self.node1 = A[0]
                    self.node2 = A[1]
                    self.writefile()
                    
    def writefile(self):
##        with open ('codefragment.c','a') as self.myfile:
        if self.node1 in St_Init_node:
            self.myfile.write("\n\nInit Node")
        if self.node1 in St_SP_node:
            self.myfile.write("\n\nStart_Send_Packet Node")
        if self.node1 in St_PI_node:
            self.myfile.write("\n\nStart_Packet_Input Node")
        if self.node1 in St_On_node:
            self.myfile.write("\n\nStart_ON_Node")
        if self.node1 in St_Off_node:
            self.myfile.write("\n\nStart_OFF_Node")
        if self.node1 in St_CCI_node:
            self.myfile.write("\n\nStart_Channel_Check_Interval Node")
        if self.node1 in Wp_node:
            self.myfile.write("\nWait for Packet Node")
        if self.node1 in Rb_node:
            self.myfile.write("\nRandom Backoff Node")
        self.myfile.write(" -----> ")
        if self.node2 in Wp_node:
            self.myfile.write("Wait for Packet Node")
        if self.node2 in Rb_node:
            self.myfile.write("Random Backoff Node")
        if self.node2 in Sp_node:
            self.myfile.write("Send Packet Node")
        if self.node2 in Rv_node:
            self.myfile.write("Return Value Node")
        if self.node2 in Cust_node:
            self.myfile.write("Custom Code Node")

    def draw_nxgraph(self):
        self.count += 1
        if self.count > 1:
            self.net.add_edges_from(codefragment)
##        self.updatePositions()
        nx.draw(self.net,with_labels = True)
        print(nx.info(self.net))
        plt.show()
        
        nx.write_gpickle(self.net,"test.gpickle")
        G = nx.read_gpickle("test.gpickle")
        print(G)

##        pickle_db = {}
##        pickle_db['codefrag'] = codefragment
##        dbfile = open('examplePickle', 'ab')
##        pickle.dump(pickle_db, dbfile)
##        dbfile.close()
##        
##        dbfile = open('examplePickle', 'rb')
##        pickle_db = pickle.load(dbfile)
##        for keys in pickle_db:
##            print(keys, '=>', pickle_db[keys])
##        dbfile.close()
            
        
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWin()
    sys.exit(app.exec_())
    

