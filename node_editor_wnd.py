import networkx as nx
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from node_scene import Scene
from node_graphics_view import QDMGraphicsView


class NodeEditorWnd(QWidget):
    def __init__(self,parent,list_flag,net,node_content):
        super().__init__(parent)
        self.list_flag = list_flag
        self.net = net
        self.node_content = node_content
        self.initUI()

    def initUI(self):
        self.setGeometry(200, 200, 800, 600)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.layout)
        self.scene = Scene()
        
        self.view =  QDMGraphicsView(self.scene.grScene,self.scene,self.net,self.node_content,self.list_flag,self)

        self.layout.addWidget(self.view)
        self.setWindowTitle("Node Editor")
        self.show()

