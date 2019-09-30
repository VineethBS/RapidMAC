from node_graphics_edge import *
##from nodeEditor_main import savebuttonClicked


EDGE_TYPE_DIRECT = 1
EDGE_TYPE_BEZIER = 2

DEBUG = False
codefragment = {}
codefrag_node = []
NODE_1 = 0


class Edge:
    def __init__(self,scene,start_socket,end_socket, edge_type=EDGE_TYPE_DIRECT):
        self.scene = scene
        
        self.start_socket = start_socket
        self.end_socket = end_socket

        self.start_socket.edge = self
        if self.end_socket is not None:
            self.end_socket.edge = self

        self.grEdge = QDMGraphicsEdgeDirect(self) if edge_type==EDGE_TYPE_DIRECT else QDMGraphicsEdgeBezier(self)

        self.updatePositions()

##        print("Edge:", self.grEdge.posSource, "to", self.grEdge.posDestination)
         
        self.scene.grScene.addItem(self.grEdge)
        self.scene.addEdge(self)

    def __str__(self):
        return "<Edge %s..%s>" % (hex(id(self))[2:5], hex(id(self))[-3:])

    def updatePositions(self):
        source_pos = self.start_socket.getSocketPosition()
        source_pos[0] += self.start_socket.node.grNode.pos().x()
        source_pos[1] += self.start_socket.node.grNode.pos().y()
##        codefrag_node.append(self.start_socket.node.grNode)
##        print("Start Node Socket: (",self.start_socket.node.grNode.pos().x(),
##              ",",self.start_socket.node.grNode.pos().y(),")")
        self.grEdge.setSource(*source_pos)
              
        if self.end_socket is not None:
            end_pos = self.end_socket.getSocketPosition()
            hex_val = hex(id(self.start_socket.node.grNode))[-3:]
##            print('self.end_socket.node.grNode:',self.end_socket.node.grNode)
            codefragment[hex_val] = hex(id(self.end_socket.node.grNode))[-3:]
##            codefrag_node.append(self.start_socket.node.grNode)
##            codefrag_node.append(self.end_socket.node.grNode)
##            NODE_1 = self.start_socket.node.grNode
#            self.savebuttonClicked()
            print('start node: ',hex(id(self.start_socket.node.grNode))[-3:])
            print('end node: ',hex(id(self.end_socket.node.grNode))[-3:])
##            codefragment['self.start_socket.node.grNode'] = self.end_socket.node.grNode
            end_pos[0] += self.end_socket.node.grNode.pos().x()
            end_pos[1] += self.end_socket.node.grNode.pos().y()
##            print("End Node Socket: (",self.end_socket.node.grNode.pos().x(),",",
##                  self.end_socket.node.grNode.pos().y(),")")
            self.grEdge.setDestination(*end_pos)
        else:
            self.grEdge.setDestination(*source_pos)
        
##        print("SS:", self.start_socket)
##        print("ES:", self.end_socket)
        self.grEdge.update()
        print('codefragment = ',codefragment)

    def remove_from_sockets(self):
        if self.start_socket is not None:
            self.start_socket.edge = None
        if self.end_socket is not None:
            self.end_socket.edge = None
        self.end_socket = None
        self.start_socket = None

    def remove(self):
        self.remove_from_sockets()
        self.scene.grScene.removeItem(self.grEdge)
        self.grEdge = None
        self.scene.removeEdge(self)
        


        
        

