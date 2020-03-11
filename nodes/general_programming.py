from PyQt5.QtCore import *
from rapidmac_conf import *
from rapidmac_node_base import *
from nodeeditor.utils import dumpException

#################################### Expression ##################################
class RAPMAC_Expression_Content(QDMNodeContentWidget):
    def initUI(self):
        self.expression = QLineEdit("x = y", self)
        self.expression.setAlignment(Qt.AlignLeft)
        self.expression.setObjectName(self.node.content_label_objname)
    
    def serialize(self):
        res = super().serialize()
        res['expression'] = self.expression.text()
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        try:
            value = data['expression']
            self.expression.setText(value)
            return True & res
        except Exception as e:
            dumpException(e)
        return res

@register_node(OP_NODE_EXPRESSION)
class RAPMACNode_Expression(RAPMACNode):
    icon = "icons/in.png"
    op_code = OP_NODE_EXPRESSION
    op_title = "Expression"
    content_label_objname = "node_expression"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[1])
        self.eval()

    def initInnerClasses(self):
        self.content = RAPMAC_Expression_Content(self)
        self.grNode = RAPMACGraphicsNode(self)
        self.content.expression.textChanged.connect(self.onInputChanged)

    def evalImplementation(self):
        pass

#################################### Variable ##################################

class RAPMAC_Variable_Content(QDMNodeContentWidget):
    def initUI(self):
        self.expression = QLineEdit("char", self)
        self.expression.setAlignment(Qt.AlignRight)
        self.expression.setObjectName(self.node.content_label_objname + ".type")
        self.variable_name = QLineEdit("variable", self)
        self.variable_name.setAlignment(Qt.AlignRight)
        self.variable_name.setObjectName(self.node.content_label_objname + ".name")
        self.input_layout = QVBoxLayout()
        self.input_layout.addWidget(self.expression)
        self.input_layout.addWidget(self.variable_name)
        self.setLayout(self.input_layout)

    def serialize(self):
        res = super().serialize()
        res['type'] = self.expression.text()
        res['name'] = self.variable_name.text()
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        try:
            value = data['type']
            self.expression.setText(value)
            value = data['name']
            self.variable_name.setText(value)
            return True & res
        except Exception as e:
            dumpException(e)
        return res

class RAPMAC_Variable_GraphicsNode(RAPMACGraphicsNode):
    def initSizes(self):
        super().initSizes()
        self.width = 160
        self.height = 120
        self.edge_roundness = 6
        self.edge_padding = 0
        self.title_horizontal_padding = 8
        self.title_vertical_padding = 10


@register_node(OP_NODE_VARIABLE)
class RAPMACNode_Variable(RAPMACNode):
    icon = "icons/in.png"
    op_code = OP_NODE_VARIABLE
    op_title = "Variable "
    content_label_objname = "node_variable"

    def __init__(self, scene):
        super().__init__(scene, inputs=[], outputs=[3])
        self.eval()

    def initInnerClasses(self):
        self.content = RAPMAC_Variable_Content(self)
        self.grNode = RAPMAC_Variable_GraphicsNode(self)
        self.content.expression.textChanged.connect(self.onInputChanged)
        self.content.variable_name.textChanged.connect(self.onInputChanged)

    def evalImplementation(self):
        pass