from node_graphics_node import QDMGraphicsNode
from node_content_widget import QDMNodeContentWidget
from node_socket import *

codefragmenttext = []
St_node = []
Wp_node = []
Rb_node = []
Sp_node = []

class Node():
    def __init__(self,scene,title="New Node",inputs=[], outputs=[]):
        print('*----node_node----*')
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

#        self.data = data
        self.next = None
        self.prev = None

        counter = 0
        for item in self.nodeinputs:
            socket = Socket(node=self, index=counter, position=LEFT_TOP, socket_type=item)      # ** position changed from LEFT_BOTTOM to LEFT_TOP
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
            # start from bottom
            y = self.grNode.height - self.grNode.edge_size - self.grNode._padding - index * self.socket_spacing
        else :
            # start from top
            y = self.grNode.title_height + self.grNode._padding + self.grNode.edge_size + index * self.socket_spacing

        return [x, y]

    def updateConnectedEdges(self):
        for socket in self.inputs + self.outputs:
            if socket.hasEdge():
                socket.edge.updatePositions()

class Start_Node(Node):
    def __init__(self,scene,title="Start Node",inputs=[],outputs=[],name_t=None):
        print("Derived Class - Start Node")
        Node.__init__(self,scene,title="Start Node",inputs=[], outputs=[1])
        self.name_t = name_t
#        self.data = data
##        self.prev = None
        St_node.append(hex(id(self.grNode))[-3:])
        print("node_node--> St_node[] = ", St_node)
        codefragmenttext.append("Start Node")

class Waitforpkt_Node(Node):
    def __init__(self,scene,title="Wait for packet Node",inputs=[],outputs=[],name_w=None):
        print("Derived Class - Wait for packet Node")
        Node.__init__(self,scene,title="Wait for packet Node",inputs=[1], outputs=[1])
        self.name_w = name_w
        Wp_node.append(hex(id(self.grNode))[-3:])
        codefragmenttext.append("Wait for packet Node")

class Randombackoff_Node(Node):
    def __init__(self,scene,title="Randombackoff Node",inputs=[],outputs=[],name_r=None):
        print("Derived class - Randombackoff_Node")
        Node.__init__(self,scene,title="Random backoff Node",inputs=[1,2], outputs=[1])
        self.name_r = name_r
        Rb_node.append(hex(id(self.grNode))[-3:])
        codefragmenttext.append("Random Backoff Node")

class Sendpacket_Node(Node):
    def __init__(self,scene,title="Sendpacket Node",inputs=[],outputs=[],name_s=None):
        print("Derived class - Sendpacket_Node")
        Node.__init__(self,scene,title="Send packet Node",inputs=[1,2,3], outputs=[1])
        self.name_s = name_s
        Sp_node.append(hex(id(self.grNode))[-3:])
        codefragmenttext.append("Sendpacket Node")


         
