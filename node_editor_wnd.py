from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from node_scene import Scene
from node_node import Node,Start_Node,Waitforpkt_Node,Randombackoff_Node,Sendpacket_Node
from node_graphics_view import QDMGraphicsView
from node_edge import Edge, EDGE_TYPE_BEZIER

nodeid = []

class NodeEditorWnd(QWidget):
    def __init__(self,parent,list_flag):
        print('*----node_editor_wnd----*')
        super().__init__(parent)
        self.list_flag = list_flag
        self.initUI()

    def initUI(self):
        self.setGeometry(200, 200, 800, 600)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.layout)

        self.scene = Scene()

##                self.addNodes()
        self.create_nodes()     # to create our nodes

        self.view =  QDMGraphicsView(self.scene.grScene,self)

        self.layout.addWidget(self.view)
        self.setWindowTitle("Node Editor")
        self.show()

    def mousePressEvent(self,event):
        print('Hitting node_editor_wnd - MPE')
        if event.button() == Qt.LeftButton:
            self.point = event.pos()
            self.create_nodes()

    def create_nodes(self):
        print('create_Nodes...')
        if self.list_flag[0] == 1:
            node_st = Start_Node(self.scene,"StartNode",inputs=[],outputs=[1],name_t="node1")
            node_st.setPos(self.point.x(),self.point.y())
            nodeid.append(self.list_flag[0])

        if self.list_flag[0] == 2:
            node_wfp = Waitforpkt_Node(self.scene,"WaitforPacketNode",inputs=[1],outputs=[1],name_w="node2")
            node_wfp.setPos(self.point.x(),self.point.y())
            nodeid.append(self.list_flag[0])

        if self.list_flag[0] == 3:
            node_rb = Randombackoff_Node(self.scene,"RandomBackoffNode",inputs=[1,2],outputs=[1],name_r="node3")
            node_rb.setPos(self.point.x(),self.point.y())
            nodeid.append(self.list_flag[0])

        if self.list_flag[0] == 4:
            node_sp = Sendpacket_Node(self.scene,"SendPacketNode",inputs=[1,2,3],outputs=[1],name_s="node4")
            node_sp.setPos(self.point.x(),self.point.y())
            nodeid.append(self.list_flag[0])


    def addNodes(self):
        node1 = Node(self.scene, "My Awesome Node 1", inputs = [0,2,3], outputs = [1,2])
        node2 = Node(self.scene, "My Awesome Node 2", inputs = [0,4,5], outputs = [1,2])
        node3 = Node(self.scene, "My Awesome Node 3", inputs = [1,0,2], outputs = [1,2])
        node1.setPos(-350, -250)
        node2.setPos(-75, 0)
        node3.setPos(200,-150)
        edge1 = Edge(self.scene, node1.outputs[0],node2.inputs[0],edge_type=EDGE_TYPE_BEZIER)
        edge2 = Edge(self.scene, node2.outputs[0],node3.inputs[0],edge_type=EDGE_TYPE_BEZIER)
#              edge3 = Edge(self.scene, node1.outputs[0],node3.inputs[1],edge_type=EDGE_TYPE_BEZIER)

    def loadStylesheet(self, filename):
        print('STYLE loading:', filename)
        file = QFile(filename)
        file.open(QFile.ReadOnly | QFile.Text)
        stylesheet = file.readAll()
        QApplication.instance().setStyleSheet(str(stylesheet, encoding='utf-8'))



