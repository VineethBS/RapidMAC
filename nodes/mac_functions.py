from PyQt5.QtCore import *
from rapidmac_conf import *
from rapidmac_node_base import *
from nodeeditor.utils import dumpException


class RAPMACInputContent(QDMNodeContentWidget):
    def initUI(self):
        pass

@register_node(OP_NODE_INIT)
class Init_Node(RAPMACNode):
    icon = "icons/in.png"
    op_code = OP_NODE_INIT
    op_title = "Init"
    content_label_objname = "mac_init"
    node_type = NODE_TYPE_START

    def __init__(self, scene):
        super().__init__(scene, inputs=[], outputs=[1])
        self.eval()

    def initInnerClasses(self):
        self.content = RAPMACInputContent(self)
        self.grNode = RAPMACGraphicsNode(self)

    def evalImplementation(self):
        pass

    def get_code_string(self):
        return "init()"

@register_node(OP_NODE_SEND_PACKET)
class SendPacket_Node(RAPMACNode):
    icon = "icons/in.png"
    op_code = OP_NODE_SEND_PACKET
    op_title = "Send Packet"
    content_label_objname = "mac_send_packet"
    node_type = NODE_TYPE_START

    def __init__(self, scene):
        super().__init__(scene, inputs=[], outputs=[1])
        self.eval()

    def initInnerClasses(self):
        self.content = RAPMACInputContent(self)
        self.grNode = RAPMACGraphicsNode(self)

    def evalImplementation(self):
        pass

    def get_code_string(self):
        return "send_packet()"
