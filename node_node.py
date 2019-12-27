from node_graphics_node import QDMGraphicsNode
from node_content_widget import QDMNodeContentWidget
from node_socket import *
import networkx as nx
import matplotlib.pyplot as plt


codefragmenttext = []
St_node = []
St_Init_node = []
St_SP_node = []
St_PI_node = []
St_On_node = []
St_Off_node = []
St_CCI_node = []
Wp_node = []
Rb_node = []
Sp_node = []
Va_node = []
Fc_node = []
Rv_node = []
Cust_node = []

class Node():
    def __init__(self,scene,title="New Node",inputs=[], outputs=[]):
        self.scene = scene
        self.title = title
        self.nodeinputs = inputs
        self.nodeoutputs = outputs

        self.content = QDMNodeContentWidget()
        self.grNode = QDMGraphicsNode(self)
        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)

        self.socket_spacing = 22

        self.inputs = []
        self.outputs = []
     
        counter = 0
        for item in self.nodeinputs:
            socket = Socket(node=self, index=counter, position=LEFT_TOP, socket_type=item)  
            counter += 1
            self.inputs.append(socket)

        counter = 0
        for item in self.nodeoutputs:
            socket = Socket(node=self, index=counter, position=RIGHT_TOP,socket_type = item)
            counter += 1
            self.outputs.append(socket)

    def __str__(self):
        return "<Node %s..%s>" % (hex(id(self))[2:5], hex(id(self))[-3:])

    @property
    def pos(self):
        return self.grNode.pos()
    def setPos(self, x, y):
        self.grNode.setPos(x, y)

    def getSocketPosition(self, index, position):
        x = 0 if position in (LEFT_TOP, LEFT_BOTTOM) else self.grNode.width
        if position in (LEFT_BOTTOM, RIGHT_BOTTOM):
            y = self.grNode.height - self.grNode.edge_size - self.grNode._padding - index * self.socket_spacing
        else:
            y = self.grNode.title_height + self.grNode._padding + self.grNode.edge_size + index * self.socket_spacing

        return [x, y]

    def updateConnectedEdges(self):
        for socket in self.inputs + self.outputs:
            if socket.hasEdge():
                socket.edge.updatePositions()

class Start_Node_Init(Node):
    def __init__(self,net,node_content,scene,title="Init",inputs=[],outputs=[]):
        self.net = net
        self.node_content = node_content
        Node.__init__(self,scene,title="Init",inputs=[], outputs=[])
        St_Init_node.append(hex(id(self.grNode)))
        self.net.add_node(hex(id(self.grNode)))
        codefragmenttext.append("StartNode_Init")
        print(self.node_content)
        print('________________________________________________________________________________________')

class Start_Node_SP(Node):
    def __init__(self,net,node_content,scene,title="Send_Packet",inputs=[],outputs=[]):
        self.net = net
        self.node_content = node_content
        Node.__init__(self,scene,title="Send_Packet",inputs=[], outputs=[1])
        St_SP_node.append(hex(id(self.grNode)))
        self.net.add_node(hex(id(self.grNode)))
        codefragmenttext.append("StartNode_send_packet")
        print(self.node_content)
        print('________________________________________________________________________________________')
##        return self.node_content

class Start_Node_PI(Node):
    def __init__(self,net,node_content,scene,title="Packet_Input",inputs=[],outputs=[]):
        self.net = net
        self.node_content = node_content
        Node.__init__(self,scene,title="Packet_Input",inputs=[], outputs=[1])
        St_PI_node.append(hex(id(self.grNode)))
        self.net.add_node(hex(id(self.grNode)))
        codefragmenttext.append("StartNode_Packet_Input")
        print(self.node_content)
        print('________________________________________________________________________________________')
##        return self.node_content

class Start_Node_On(Node):
    def __init__(self,net,node_content,scene,title="On",inputs=[],outputs=[]):
        self.net = net
        self.node_content = node_content
        Node.__init__(self,scene,title="On",inputs=[], outputs=[1])
        St_On_node.append(hex(id(self.grNode)))
        self.net.add_node(hex(id(self.grNode)))
        codefragmenttext.append("StartNode_On")
        print(self.node_content)
        print('________________________________________________________________________________________')
##        return self.node_content

class Start_Node_Off(Node):
    def __init__(self,net,node_content,scene,title="Off",inputs=[],outputs=[]):
        self.net = net
        self.node_content = node_content
        Node.__init__(self,scene,title="Off",inputs=[], outputs=[1])
        St_Off_node.append(hex(id(self.grNode)))
        self.net.add_node(hex(id(self.grNode)))
        codefragmenttext.append("StartNode_Off")
        print(self.node_content)
        print('________________________________________________________________________________________')
##        return self.node_content
        
class Start_Node_CCI(Node):
    def __init__(self,net,node_content,scene,title="Channel_check_Interval",inputs=[],outputs=[]):
        self.net = net
        self.node_content = node_content
        Node.__init__(self,scene,title="Channel_check_Interval",inputs=[], outputs=[1])
        St_CCI_node.append(hex(id(self.grNode)))
        self.net.add_node(hex(id(self.grNode)))
        codefragmenttext.append("StartNode_Channel_check_Interval")
        print(self.node_content)
        print('________________________________________________________________________________________')
##        return self.node_content
        
class Waitforpkt_Node(Node):
    def __init__(self,net,node_content,scene,title="Wait for packet Node",inputs=[],outputs=[]):
        self.net = net
        self.node_content = node_content
        Node.__init__(self,scene,title="Wait for packet Node",inputs=[1], outputs=[1])
        Wp_node.append(hex(id(self.grNode)))
        self.net.add_node(hex(id(self.grNode)))
        codefragmenttext.append("Wait for packet Node")
        print(self.node_content)
        print('________________________________________________________________________________________')
        

class Randombackoff_Node(Node):
    def __init__(self,net,node_content,scene,title="Randombackoff Node",inputs=[],outputs=[]):
        self.net = net
        self.node_content = node_content
        Node.__init__(self,scene,title="Random backoff Node",inputs=[1,2], outputs=[1])
        Rb_node.append(hex(id(self.grNode)))
        self.net.add_node(hex(id(self.grNode)))
        codefragmenttext.append("Random Backoff Node")
        print(self.node_content)
        print('________________________________________________________________________________________')

class Sendpacket_Node(Node):
    def __init__(self,net,node_content,scene,title="Sendpacket Node",inputs=[],outputs=[]):
        self.net = net
        self.node_content = node_content
        Node.__init__(self,scene,title="Send packet Node",inputs=[1,2,3], outputs=[1])
        Sp_node.append(hex(id(self.grNode)))
        self.net.add_node(hex(id(self.grNode)))
        codefragmenttext.append("Sendpacket Node")
        print(self.node_content)
        print('________________________________________________________________________________________')

class ReturnValue_Node(Node):
    def __init__(self,net,node_content,scene,title="Return Value Node",inputs=[],outputs=[]):
        self.net = net
        self.node_content = node_content
        Node.__init__(self,scene,title="Return Value Node",inputs=[1], outputs=[])
        Rv_node.append(hex(id(self.grNode)))
        self.net.add_node(hex(id(self.grNode)))
        codefragmenttext.append("Return Value Node")
        print(self.node_content)
##        print(self.ret_node_content)
        print('________________________________________________________________________________________')


class FunctionCall_Node(Node):
    def __init__(self,net,node_content,scene,title="Function Call Node",inputs=[],outputs=[]):
        self.net = net
        self.node_content = node_content
        Node.__init__(self,scene,title="Function Call Node",inputs=[1], outputs=[1])
        Fc_node.append(hex(id(self.grNode)))
        self.net.add_node(hex(id(self.grNode)))
        codefragmenttext.append("Function Call Node")
        print(self.node_content)
        print('________________________________________________________________________________________')


class VariableAssign_Node(Node):
    def __init__(self,net,node_content,scene,title="Variable Assignment Node",inputs=[],outputs=[]):
        self.net = net
        self.node_content = node_content
        Node.__init__(self,scene,title="Variable Assignment Node",inputs=[1], outputs=[1])
        Va_node.append(hex(id(self.grNode)))
        self.net.add_node(hex(id(self.grNode)))
        codefragmenttext.append("Variable Assignment Node")
        print(self.node_content)
        print('________________________________________________________________________________________')

class CustomCode_Node(Node):
    def __init__(self,net,node_content,scene,title="Custom Code Node",inputs=[],outputs=[]):
        self.net = net
        self.node_content = node_content
        Node.__init__(self,scene,title="Custom Code Node",inputs=[1], outputs=[1])
        Cust_node.append(hex(id(self.grNode)))
        self.net.add_node(hex(id(self.grNode)))
        codefragmenttext.append("Custom Code Node")
        print(self.node_content)
        print('________________________________________________________________________________________')



         
