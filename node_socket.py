from node_graphics_socket import QDMGraphicsSocket


LEFT_TOP = 1
LEFT_BOTTOM = 2
RIGHT_TOP = 3
RIGHT_BOTTOM = 4

DEBUG = False

class Socket():
    def __init__(self, node, index=0, position=LEFT_TOP,socket_type = 1):
        print('*---node_socket---*')
        self.node = node
        self.index = index
        self.position = position
        self.socket_type = socket_type

        if DEBUG: print("Socket -- creating with", self.index, self.position, "for node", self.node)
        self.grSocket = QDMGraphicsSocket(self,self.socket_type)

        self.grSocket.setPos(*self.node.getSocketPosition(index, position))

        self.edge = None

    def __str__(self):
        return "<Socket %s..%s>" % (hex(id(self))[2:5], hex(id(self))[-3:])

    def getSocketPosition(self):
        print('*---node_socket--(getSocketPosition)-*')
#        print("  GSP:  ", self.index, self.position, "node:",self.node)
        res = self.node.getSocketPosition(self.index, self.position)
#        print("res:",res)
        return res 

    def setConnectedEdge(self, edge=None):
        print('*---node_socket--(setConnectedEdge)-*')
        self.edge = edge

    def hasEdge(self):
##        print('*---node_socket--(hasEdge)-*')
        return self.edge is not None
    


