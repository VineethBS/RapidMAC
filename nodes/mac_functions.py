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
        return "static void init(void)"

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
        return "static void send_packet(mac_callback_t sent, void *ptr)"

@register_node(OP_NODE_PACKET_INPUT)
class PacketInput_Node(RAPMACNode):
    icon = "icons/in.png"
    op_code = OP_NODE_PACKET_INPUT
    op_title = "Packet Input"
    content_label_objname = "mac_packet_input"
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
        return "static void packet_input(void)"

@register_node(OP_NODE_ON)
class On_Node(RAPMACNode):
    icon = "icons/in.png"
    op_code = OP_NODE_ON
    op_title = "Radio On"
    content_label_objname = "mac_on"
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
        return "static int on(void)"

@register_node(OP_NODE_OFF)
class Off_Node(RAPMACNode):
    icon = "icons/in.png"
    op_code = OP_NODE_OFF
    op_title = "Radio Off"
    content_label_objname = "mac_off"
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
        return "static int off(int keep_radio_on)"

@register_node(OP_NODE_CCI)
class CCI_Node(RAPMACNode):
    icon = "icons/in.png"
    op_code = OP_NODE_CCI
    op_title = "Channel check interval"
    content_label_objname = "channel_check_interval"
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
        return "static unsigned short channel_check_interval(void)"


######################################################################
############################ MAC Driver ##############################
######################################################################

class RAPMAC_MACDriver_Content(QDMNodeContentWidget):
    def initUI(self):
        self.macdriver_name = ""
        self.macdriver_description = ""

        self.macdriver_name_l = QLabel("Driver Name", self)
        self.macdriver_description_l = QLabel("Description", self)
        self.macdriver_name_e = QLineEdit("_driver", self)
        self.macdriver_name_e.setMinimumWidth(150)
        self.macdriver_description_e = QLineEdit("", self)
        self.macdriver_description_e.setMinimumWidth(150)

        self.input_layout = QGridLayout()
        self.input_layout.addWidget(self.macdriver_name_l, 0, 0, 1, 1)
        self.input_layout.addWidget(self.macdriver_name_e, 0, 1, 1, 2)
        self.input_layout.addWidget(self.macdriver_description_l, 1, 0, 1, 1)
        self.input_layout.addWidget(self.macdriver_description_e, 1, 1, 1, 2)

        self.macdriver_name_e.textChanged.connect(self.onInputChanged)
        self.macdriver_description_e.textChanged.connect(self.onInputChanged)

        self.setLayout(self.input_layout)

    def onInputChanged(self):
        self.macdriver_name = self.macdriver_name_e.text()
        self.macdriver_description = self.macdriver_description_e.text()

    def serialize(self):
        res = super().serialize()
        res['name'] = self.macdriver_name
        res['description'] = self.macdriver_description
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        try:
            value = data['name']
            self.macdriver_name_e.setText(value)
            self.macdriver_name = value
            value = data['description']
            self.macdriver_description_e.setText(value)
            self.macdriver_description = value
            return True & res
        except Exception as e:
            dumpException(e)
        return res

@register_node(OP_NODE_MACDRIVER)
class MACDriver_Node(RAPMACNode):
    icon = "icons/in.png"
    op_code = OP_NODE_MACDRIVER
    op_title = "MAC driver"
    content_label_objname = "mac_driver"
    node_type = NODE_TYPE_START

    def __init__(self, scene):
        super().__init__(scene, inputs=[], outputs=[])
        self.eval()

    def initInnerClasses(self):
        self.content = RAPMAC_MACDriver_Content(self)
        self.grNode = RAPMACGraphicsNode(self)
        self.grNode.width = 250
        self.grNode.height = 100

    def evalImplementation(self):
        pass

    def get_code_string(self):
        code_string = """
        const struct mac_driver %s = {
            "%s",
            init,
            send_packet,
            packet_input,
            on,
            off,
            channel_check_interval,
        };
        """ % (self.content.macdriver_name, self.content.macdriver_description)
        return code_string

