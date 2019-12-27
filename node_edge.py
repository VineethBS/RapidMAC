from node_graphics_edge import *
import networkx as nx

EDGE_TYPE_DIRECT = 1
EDGE_TYPE_BEZIER = 2

DEBUG = False

codefragment = []
edge_startnode = []
edge_endnode = []

NODE_1 = 0


class Edge:
    def __init__(self,scene,net,start_socket,end_socket, edge_type=EDGE_TYPE_BEZIER):
        self.scene = scene
        self.net = net
        self.start_socket = start_socket
        self.end_socket = end_socket

        self.start_socket.edge = self
        if self.end_socket is not None:
            self.end_socket.edge = self

        self.grEdge = QDMGraphicsEdgeDirect(self) if edge_type==EDGE_TYPE_DIRECT else QDMGraphicsEdgeBezier(self)
        self.updatePositions()
        
        self.scene.grScene.addItem(self.grEdge)
        self.scene.addEdge(self)

    def __str__(self):
        return "<Edge %s..%s>" % (hex(id(self))[2:5], hex(id(self))[-3:])

    def updatePositions(self):
        if self.start_socket is not None:
            source_pos = self.start_socket.getSocketPosition()
            source_pos[0] += self.start_socket.node.grNode.pos().x()
            source_pos[1] += self.start_socket.node.grNode.pos().y()

        self.grEdge.setSource(*source_pos)
        
        if self.end_socket is not None:
            end_pos = self.end_socket.getSocketPosition()
            end_pos[0] += self.end_socket.node.grNode.pos().x()
            end_pos[1] += self.end_socket.node.grNode.pos().y()
            self.edge_startnode = hex(id(self.start_socket.node.grNode)) 
            self.edge_endnode = hex(id(self.end_socket.node.grNode))  
            
            codefragment.append((self.edge_startnode,self.edge_endnode))

            self.net.add_edge(hex(id(self.start_socket.node.grNode)),hex(id(self.end_socket.node.grNode)))
            
            L = len(codefragment)
        
            if L > 1:
                for a in range (0,L-1):
                    
                    if ((codefragment[a][0] == self.edge_startnode) and (codefragment[a][1] == self.edge_endnode)):
                        del codefragment[-1]
                        self.net.remove_edge(hex(id(self.start_socket.node.grNode)),hex(id(self.end_socket.node.grNode)))
                        
            self.grEdge.setDestination(*end_pos)
        else:
            self.grEdge.setDestination(*source_pos)
        self.grEdge.update()
        
        return self.net
        

    def remove_from_sockets(self):
        if self.start_socket is not None:
            self.start_socket.edge = None
        if self.end_socket is not None:
            self.end_socket.edge = None
        self.net.remove_edge(hex(id(self.start_socket.node.grNode)),hex(id(self.end_socket.node.grNode)))
        self.end_socket = None
        self.start_socket = None
        codefragment.remove((self.edge_startnode,self.edge_endnode))


    def remove(self):
        self.remove_from_sockets()
        self.scene.grScene.removeItem(self.grEdge)
        self.grEdge = None
        self.scene.removeEdge(self)


