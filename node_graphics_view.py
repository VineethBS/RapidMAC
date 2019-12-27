from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QGraphicsView,QMessageBox,QApplication,QWidget,QInputDialog,QLineEdit,QAction,QPlainTextEdit,QTextEdit,QVBoxLayout,QFrame,QPushButton
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.Qt import QApplication, QClipboard
from node_graphics_node import QDMGraphicsNode
from node_graphics_socket import QDMGraphicsSocket
from node_graphics_edge import QDMGraphicsEdge
from node_edge import Edge, EDGE_TYPE_BEZIER
from node_node import Node,Start_Node_Init,Start_Node_SP,Start_Node_PI,Start_Node_On,Start_Node_Off,Start_Node_CCI
from node_node import Waitforpkt_Node,Randombackoff_Node,Sendpacket_Node,ReturnValue_Node,FunctionCall_Node,VariableAssign_Node,CustomCode_Node
from node_node import Rv_node, Cust_node
import sys
import networkx as nx

INIT_content = "static void\ninit(void)\n{\n}"
SP_content = "static void \nsend_packet(mac_callback_t sent, void *ptr)\n{\n\tp.sent = sent;\
                \n\tp.ptr = ptr;\n\tclock_time_t delay = random_rand() % CLOCK_SECOND;\
                \n\tPRINTF('Simple-ALOHA : at %u scheduling transmission in %u ticks\\n', (unsigned) clock_time(),(unsigned) delay);\
                \n\tctimer_set(&transmit_timer, delay, _send_packet, &p);\n\tsent(ptr, MAC_TX_DEFERRED, 1);\n}"
PI_content = "static void \npacket_input(void)\n{\n\tNETSTACK_LLSEC.input();\n}"
ON_content1 = "static int\non(void)\n{\n\t"
ON_content2 = ";\n}"
OFF_content1 = "static int\noff(int keep_radio_on)\n{\n\t"
OFF_content2 = ";\n}"
CCI_content1 = "static unsigned short\nchannel_check_interval(void)\n{\n\t"
CCI_content2 = ";\n}"

Ret_textinputs = []
Custom_textinputs = []

MODE_NOOP = 1
MODE_EDGE_DRAG = 2
EDGE_DRAG_START_THRESHOLD = 10
DEBUG = False

class Textbox(QWidget):
    def __init__(self,custom_node):
        super().__init__()
        self.custom_node = custom_node
        self.title = "Enter your code here:"
        self.top = 250
        self.left = 250
        self.width = 350
        self.height = 300
        self.widget_method()

    def widget_method(self):
        self.setWindowTitle(self.title)
        self.resize(self.width, self.height)
        self.move(self.left, self.top)
        
        self.frame1 = QFrame(self)
        self.frame1.setGeometry(QRect(40, 40, 300, 180))
        
        self.text_edit1 = QTextEdit(self.frame1)
        self.text_edit1.move(0, 0)
        self.text_edit1.setAcceptRichText(False)

        if len(Custom_textinputs) != 0:
            for a in range (len(Custom_textinputs)):
                temp = Custom_textinputs[len(Custom_textinputs)-1-a]
                if self.custom_node == temp[0]:
                    display_text = temp[1]
                    self.text_edit1.append(display_text)
                    break
                else:
                    continue
        
        button = QPushButton('OK', self)
##        button.resize(100,32)
        button.move(250, 250) 
        button.clicked.connect(self.savetext)
        
        self.show()
        

    def savetext(self):
        print("OK button clicked")
        self.close()
        self.textvalue = self.text_edit1.document().toPlainText()
##        self.textvalue = self.text_edit1.toPlainText()
        if len(Custom_textinputs) != 0:
            for a in range (len(Custom_textinputs)):
                temp = Custom_textinputs[a]
                if self.custom_node == temp[0]:
##                    temp[1] = self.textvalue
                    Custom_textinputs.remove(Custom_textinputs[a])
##                    Custom_textinputs.append((self.custom_node,self.textvalue))
                    break
                else:
                    continue
        Custom_textinputs.append((self.custom_node,self.textvalue))
        print(self.textvalue)
        return self.textvalue
        
class QDMGraphicsView(QGraphicsView):
    def __init__(self, grScene,scene, net, node_content, list_flag, parent=None):
        super().__init__(parent)
        self.grScene = grScene
        self.scene = scene
        self.net = net
        self.node_content = node_content
##        self.nodename = nodename
        self.list_flag = list_flag
##        self.textbox = QLineEdit(self)
##        self.startnode = 0
        self.st_init = 0
        self.st_sp = 0
        self.st_pi = 0
        self.st_on = 0
        self.st_off = 0
        self.st_cci = 0
        self.initUI()

        self.setScene(self.grScene)

        self.mode = MODE_NOOP

        self.zoomInFactor = 1.25
        self.zoomClamp = True
        self.zoom = 10
        self.zoomStep = 1
        self.zoomRange = [0, 10]

        return 

    def initUI(self):
        self.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing | 
                    QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

    def mousePressEvent(self,event):
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonPress(event)
        elif event.button() == Qt.LeftButton:
            self.leftMouseButtonPress(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonPress(event)
        else:
            super().mousePressEvent(event)


    def mouseReleaseEvent(self,event):
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonRelease(event)
        elif event.button() == Qt.LeftButton:
            self.leftMouseButtonRelease(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonRelease(event)
        else:
            super().mouseReleaseEvent(event)

    def middleMouseButtonPress(self, event):
        releaseEvent = QMouseEvent(QEvent.MouseButtonRelease, event.localPos(), event.screenPos(),
                        Qt.LeftButton, Qt.NoButton, event.modifiers())
        super().mouseReleaseEvent(releaseEvent)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                    Qt.LeftButton, event.buttons() | Qt.LeftButton, event.modifiers())
        super().mousePressEvent(fakeEvent)

    def middleMouseButtonRelease(self,event):
        fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                    Qt.LeftButton, event.buttons() & -Qt.LeftButton, event.modifiers())
        super().mouseReleaseEvent(fakeEvent)
        self.setDragMode(QGraphicsView.NoDrag)

    def leftMouseButtonPress(self,event):
        item = self.getItemAtClick(event)

        if item is None:
            p = self.mapToScene(event.pos())
            self.create_nodes(p)

        self.last_lmb_click_scene_pos = self.mapToScene(event.pos())

        if type(item) is QDMGraphicsSocket:
            if self.mode == MODE_NOOP:
                self.mode = MODE_EDGE_DRAG
                self.edgeDragStart(item)
                return

        if self.mode == MODE_EDGE_DRAG:
            res = self.edgeDragEnd(item)
            if res: return

        super().mousePressEvent(event)

    def leftMouseButtonRelease(self, event):
        item = self.getItemAtClick(event)

        if self.mode == MODE_EDGE_DRAG:
            if self.distanceBetweenClickAndReleaseIsOff(event):
                res = self.edgeDragEnd(item)
                if res: return

        super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event):
        item = self.getItemAtClick(event)
        print("\n............................\nhex(id(item)) = ",hex(id(item)))
        print("Cust_node = ",Cust_node)
        print("Rv_node = ",Rv_node)
        if type(item) is QDMGraphicsNode:
            if (hex(id(item))) in Rv_node:
##                return_txt = QLineEdit()
                text, okPressed = QInputDialog.getText(self, "Return Value ?","Enter the return value:", QLineEdit.Normal, "")  
                if okPressed and text != '':
##                    textLabel->setText(text)
##                    return_txt.setText(text)
                    print(text)
                    for t in range (len(Ret_textinputs)):
                        temp = Ret_textinputs[t]
                        if (hex(id(item))) == temp[0]:
                            Ret_textinputs.remove(Ret_textinputs[t])
                            print("********** Ret_textinput - removed ************")
                            break
                        else:
                            continue
                    Ret_textinputs.append((hex(id(item)),text))
            if (hex(id(item))) in Cust_node:
##                main_window = QMainWindow()
##                text_edit_widget = QPlainTextEdit()
##                text_edit_widget.setStyleSheet(
##                    """QPlainTextEdit {background-color: #fff;
##                           color: #000000;
##                           font-family: Courier;}""")
##                main_window.setCentralWidget(text_edit_widget)
##                main_window.show()
##                self.text_edit1.textChanged.connect(self.savetext)
##
##    def savetext(self):
##        textvalue = self.text_edit1.document().toPlainText()
##        print('--------------------\n',textvalue)
                
                display_textbox = Textbox(hex(id(item)))
                display_textbox.show()
                show(self)
                

##                print('self.textvalue = ',self.textvalue)
##                print('Support print')
##                self.Show()
##                display_textbox.show(True)
                
##                text_edit_widget = QPlainTextEdit()
##                text_edit_widget.setStyleSheet(
##                    """QPlainTextEdit {background-color: #333;
##                           color: #00FF00;
##                           text-decoration: underline;
##                           font-family: Courier;}""")
####                self.setCentralWidget(text_edit_widget)
##                text_edit_widget.textChanged.connect(
##                    lambda: print(text_edit_widget.document().toPlainText()))
##                text_edit_widget.document().setPlainText("Enter your code here")
                
##                QTextEdit* textbox = QTextEdit(self)
##                QApplication::clipboard()->clear (QClipboard::Clipboard)
##                textbox->copy()
##                const QString clipSel2 = QApplication::clipboard()->text (QClipboard::Clipboard)
##                print(clipSel2)
##                self.textbox = QTextEdit(hex(id(item)))
##                self.textbox.move(150,150)
##                self.textbox.resize(280,40)
##                self.tbox = QPlainTextEdit(self)
##                self.tbox.insertPlainText("Enter your code here: \n")
##                self.tbox.move(event.pos.x(), event.pos.y())
##                self.tbox.resize(400,200)
##                textboxValue = self.textbox.text()
##                QMessageBox.question(self, 'Enter the Custom Code', "You Entered: " + textboxValue, QMessageBox.Ok, QMessageBox.Ok)
##                self.textbox.setText("")
##                Custom_textinputs.append((hex(id(item)),self.textbox))
                
                    
##            if type(item) is ReturnValue_Node:
##                text, okPressed = QInputDialog.getText(self, "Return Value ?","Enter the return value:", QLineEdit.Normal, "")
##                if okPressed and text != '':
##                    print(text)
        print(Ret_textinputs)
        print(Custom_textinputs)
        
    def mouseMoveEvent(self, event):
##        print('.....node_graphics_view : mouseMoveEvent')
        if self.mode == MODE_EDGE_DRAG:
            pos = self.mapToScene(event.pos())
            self.dragEdge.grEdge.setDestination(pos.x(), pos.y())
            self.dragEdge.grEdge.update()

        super().mouseMoveEvent(event)
  
    def getItemAtClick(self, event):
        """ return the object on which we've clicked/release mouse button """
        pos = event.pos()
        obj = self.itemAt(pos)
        return obj

    def edgeDragStart(self, item):
        if DEBUG: print('View::edgeDragStart ~ Start dragging edge')
        if DEBUG: print('View::edgeDragStart ~   assign Start Socket')
        if DEBUG: print('View::edgeDragStart ~   assign Start Socket to:', item.socket)
        self.previousEdge = item.socket.edge
        self.last_start_socket = item.socket
        self.dragEdge = Edge(self.grScene.scene, self.net, item.socket, None, EDGE_TYPE_BEZIER)
        if DEBUG: print('View::edgeDragStart ~   dragEdge:', self.dragEdge)

    def edgeDragEnd(self, item):
        """ return True if skip the rest of the code """
        self.mode = MODE_NOOP
        if type(item) is QDMGraphicsSocket:
            if DEBUG: print('View::edgeDragEnd ~   previous edge:', self.previousEdge)
            if item.socket.hasEdge():
                item.socket.edge.remove()
            if DEBUG: print('View::edgeDragEnd ~   assign End Socket', item.socket)
            if self.previousEdge is not None: self.previousEdge.remove()
            if DEBUG: print('View::edgeDragEnd ~  previous edge removed')
            self.dragEdge.start_socket = self.last_start_socket
            self.dragEdge.end_socket = item.socket
            self.dragEdge.start_socket.setConnectedEdge(self.dragEdge)
            self.dragEdge.end_socket.setConnectedEdge(self.dragEdge)
            
            if DEBUG: print('View::edgeDragEnd ~  reassigned start & end sockets to drag edge')
            self.dragEdge.updatePositions()
            return True
        if DEBUG: print('View::edgeDragEnd ~ End dragging edge')
        self.dragEdge.remove()
        self.dragEdge = None
        if DEBUG: print('View::edgeDragEnd ~ about to set socket to previous edge:', self.previousEdge)
        if self.previousEdge is not None:
            self.previousEdge.start_socket.edge = self.previousEdge
        if DEBUG: print('View::edgeDragEnd ~ everything done.')
        return False

    def distanceBetweenClickAndReleaseIsOff(self, event):
        """ measures if we are too far from the last LMB click scene position """
        new_lmb_release_scene_pos = self.mapToScene(event.pos())
        dist_scene = new_lmb_release_scene_pos - self.last_lmb_click_scene_pos
        edge_drag_threshold_sq = EDGE_DRAG_START_THRESHOLD*EDGE_DRAG_START_THRESHOLD
        return (dist_scene.x()*dist_scene.x() + dist_scene.y()*dist_scene.y()) > edge_drag_threshold_sq

    def wheelEvent(self,event):
        zoomOutFactor = 1/self.zoomInFactor

        if event.angleDelta().y() > 0:
            zoomFactor = self.zoomInFactor
            self.zoom += self.zoomStep
        else:
            zoomFactor = zoomOutFactor
            self.zoom -= self.zoomStep

        clamped = False
        if (self.zoom < self.zoomRange[0]):
            self.zoom, clamped = self.zoomRange[0], True
        if (self.zoom > self.zoomRange[1]):
            self.zoom, clamped = self.zoomRange[1], True

        if not clamped or self.zoomClamp is False:
            self.scale(zoomFactor, zoomFactor)

    def create_nodes(self,point):
        self.point = point 
        if self.list_flag[0] == 1:
            self.st_init += 1
            self.node_content = INIT_content
            if self.st_init > 1:
                QMessageBox.about(self, "Init node !", "Only one Init node can be created !")
            else:
                node_st = Start_Node_Init(self.net,self.node_content,self.scene,"Init",inputs=[],outputs=[])
                node_st.setPos(self.point.x(),self.point.y())
                
        if self.list_flag[0] == 2:
            self.st_sp += 1
            self.node_content = SP_content
            if self.st_sp > 1:
                QMessageBox.about(self, "Send_Packet node !", "Only one Send_Packet node can be created !")
            else:
                node_st = Start_Node_SP(self.net,self.node_content,self.scene,"Send_Packet",inputs=[],outputs=[1])
                node_st.setPos(self.point.x(),self.point.y())
                
        if self.list_flag[0] == 3:
            self.st_pi += 1
            self.node_content = PI_content
            if self.st_pi > 1:
                QMessageBox.about(self, "Packet_Input node !", "Only one Packet_Input node can be created !")
            else:
                node_st = Start_Node_PI(self.net,self.node_content,self.scene,"Packet_Input",inputs=[],outputs=[1])
                node_st.setPos(self.point.x(),self.point.y())
                
        if self.list_flag[0] == 4:
            self.st_on += 1
            self.node_content = ON_content1 + ON_content2
            if self.st_on > 1:
                QMessageBox.about(self, "ON node !", "Only one ON node can be created !")
            else:
                node_st = Start_Node_On(self.net,self.node_content,self.scene,"ON",inputs=[],outputs=[1])
                node_st.setPos(self.point.x(),self.point.y())
                
        if self.list_flag[0] == 5:
            self.st_off += 1
            self.node_content = OFF_content1 + OFF_content2
            if self.st_off > 1:
                QMessageBox.about(self, "OFF node !", "Only one OFF node can be created !")
            else:
                node_st = Start_Node_Off(self.net,self.node_content,self.scene,"OFF",inputs=[],outputs=[1])
                node_st.setPos(self.point.x(),self.point.y())
                
        if self.list_flag[0] == 6:
            self.st_cci += 1
            self.node_content = CCI_content1 + CCI_content2
            if self.st_cci > 1:
                QMessageBox.about(self, "Channel_Check_Interval node !", "Only one channel_check_interval node can be created !")
            else:
                node_st = Start_Node_CCI(self.net,self.node_content,self.scene,"Channel_Check_Interval",inputs=[],outputs=[1])
                node_st.setPos(self.point.x(),self.point.y())
            
        if self.list_flag[0] == 7:
            self.node_content = "Wait for Packet Node"
            node_wfp = Waitforpkt_Node(self.net,self.node_content,self.scene,"WaitforPacketNode",inputs=[1],outputs=[1])
            node_wfp.setPos(self.point.x(),self.point.y())

        if self.list_flag[0] == 8:
            self.node_content = "Random Backoff Node"
            node_rb = Randombackoff_Node(self.net,self.node_content,self.scene,"RandomBackoffNode",inputs=[1,2],outputs=[1])
            node_rb.setPos(self.point.x(),self.point.y())

        if self.list_flag[0] == 9:
            self.node_content = "Send Packet Node"
            node_sp = Sendpacket_Node(self.net,self.node_content,self.scene,"SendPacketNode",inputs=[1,2,3],outputs=[1])
            node_sp.setPos(self.point.x(),self.point.y())

        if self.list_flag[0] == 10:
            self.node_content = "Return Value Node"
            node_return = ReturnValue_Node(self.net,self.node_content,self.scene,"ReturnValueNode",inputs=[1],outputs=[])
            node_return.setPos(self.point.x(),self.point.y())

        if self.list_flag[0] == 11:
            self.node_content = "Fuction Call Node"
            node_funcall = FunctionCall_Node(self.net,self.node_content,self.scene,"FunctionCallNode",inputs=[1],outputs=[1])
            node_funcall.setPos(self.point.x(),self.point.y())

        if self.list_flag[0] == 12:
            self.node_content = "Variable Assignment Node"
            node_varass = VariableAssign_Node(self.net,self.node_content,self.scene,"VariableAssignmentNode",inputs=[1],outputs=[1])
            node_varass.setPos(self.point.x(),self.point.y())

        if self.list_flag[0] == 13:
            self.node_content = "Custom Code Node"
            node_custom = CustomCode_Node(self.net,self.node_content,self.scene,"CustomCodeNode",inputs=[1],outputs=[1])
            node_custom.setPos(self.point.x(),self.point.y())

