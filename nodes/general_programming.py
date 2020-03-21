from PyQt5.QtCore import *
from rapidmac_conf import *
from rapidmac_node_base import *
from nodeeditor.utils import dumpException

######################################################################
###################### Preprocessor #DEFINE ##########################
######################################################################
class RAPMAC_HashDefine_Content(QDMNodeContentWidget):
    def initUI(self):
        self.expression = QLineEdit("", self)
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

@register_node(OP_NODE_DEFINE)
class RAPMACNode_Expression(RAPMACNode):
    icon = "icons/in.png"
    op_code = OP_NODE_DEFINE
    op_title = "HashDefine"
    node_type = NODE_TYPE_NORMAL
    content_label_objname = "node_hash_define"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[1])
        self.eval()

    def initInnerClasses(self):
        self.content = RAPMAC_HashDefine_Content(self)
        self.grNode = RAPMACGraphicsNode(self)
        self.content.expression.textChanged.connect(self.onInputChanged)

    def get_code_string(self):
        return "#DEFINE " + self.content.expression.text() + ";"

    def evalImplementation(self):
        pass

######################################################################
############################ Comments ################################
######################################################################
class RAPMAC_Comment_Dialog(QDialog):
    def __init__(self, parent = None):
        super(RAPMAC_Comment_Dialog, self).__init__(parent)
        
        self.parent = parent

        self.setWindowTitle("Edit comment")
        self.textbox = QPlainTextEdit(self)
        self.textbox.setPlainText(self.parent.text)
        self.textbox.setStyleSheet("color:white")
        
        qbtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        buttonbox = QDialogButtonBox(qbtn)
        buttonbox.accepted.connect(self.accept)
        buttonbox.rejected.connect(self.reject)
        
        layout = QVBoxLayout()
        layout.addWidget(self.textbox)
        layout.addWidget(buttonbox)
        
        self.setLayout(layout)

    def accept(self):
        self.done(self.Accepted)
        self.parent.text = self.textbox.toPlainText()
        
class RAPMAC_Comment_Content(QDMNodeContentWidget):
    def initUI(self):
        self.text = ""
        self.label = QLabel(self)
        self.label.setWordWrap(True)
        self.label.setText(self.text)
        self.edit = QPushButton("Edit ...", self)
        self.edit.setObjectName(self.node.content_label_objname)
        self.edit.clicked.connect(self.onEditButtonClick)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.edit)
        self.setLayout(layout)


    def onEditButtonClick(self, s):
        dlg = RAPMAC_Comment_Dialog(self) 
        dlg.exec_()
        self.label.setText(self.text)
        
    def serialize(self):
        res = super().serialize()
        res['text'] = self.text
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        try:
            value = data['text']
            self.text = value
            return True & res
        except Exception as e:
            dumpException(e)
        return res


@register_node(OP_NODE_COMMENT)
class RAPMACNode_Comment(RAPMACNode):
    icon = "icons/in.png"
    op_code = OP_NODE_COMMENT
    op_title = "Comment"
    node_type = NODE_TYPE_NORMAL
    content_label_objname = "node_comment"

    def __init__(self, scene):
        super().__init__(scene, inputs=[], outputs=[])
        self.eval()
        self.width = 160
        self.height = 140

    def initInnerClasses(self):
        self.content = RAPMAC_Comment_Content(self)
        self.grNode = RAPMACGraphicsNode(self)

    def get_code_string(self):
        return "/* \n" + self.content.text + "\n/*"

    def evalImplementation(self):
        pass

######################################################################
##################### Multi Line Expression ##########################
######################################################################

class RAPMAC_MultiLineExpression_Dialog(QDialog):
    def __init__(self, parent = None):
        super(RAPMAC_MultiLineExpression_Dialog, self).__init__(parent)
        
        self.parent = parent

        self.setWindowTitle("Edit multiline expression")
        self.textbox = QPlainTextEdit(self)
        self.textbox.setPlainText(self.parent.text)
        self.textbox.setStyleSheet("color:white")
        
        qbtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        buttonbox = QDialogButtonBox(qbtn)
        buttonbox.accepted.connect(self.accept)
        buttonbox.rejected.connect(self.reject)
        
        layout = QVBoxLayout()
        layout.addWidget(self.textbox)
        layout.addWidget(buttonbox)
        
        self.setLayout(layout)

    def accept(self):
        self.done(self.Accepted)
        self.parent.text = self.textbox.toPlainText()

class RAPMAC_MultiLineExpression_Content(QDMNodeContentWidget):
    def initUI(self):
        self.text = ""
        self.expression = QPushButton("Edit ...", self)
        self.expression.setObjectName(self.node.content_label_objname)
        self.expression.clicked.connect(self.onEditButtonClick)

    def onEditButtonClick(self, s):
        dlg = RAPMAC_MultiLineExpression_Dialog(self) 
        dlg.exec_()
        
    def serialize(self):
        res = super().serialize()
        res['text'] = self.text
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        try:
            value = data['text']
            self.text = value
            return True & res
        except Exception as e:
            dumpException(e)
        return res

@register_node(OP_NODE_MULTILINEEXPRESSION)
class RAPMACNode_MultiLineExpression(RAPMACNode):
    icon = "icons/in.png"
    op_code = OP_NODE_MULTILINEEXPRESSION
    op_title = "Multiline"
    node_type = NODE_TYPE_NORMAL
    content_label_objname = "node_multiline"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[1])
        self.eval()

    def initInnerClasses(self):
        self.content = RAPMAC_MultiLineExpression_Content(self)
        self.grNode = RAPMACGraphicsNode(self)

    def get_code_string(self):
        return self.content.text

    def evalImplementation(self):
        pass

######################################################################
########################### Expression ###############################
######################################################################
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
    node_type = NODE_TYPE_NORMAL
    content_label_objname = "node_expression"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[1])
        self.eval()

    def initInnerClasses(self):
        self.content = RAPMAC_Expression_Content(self)
        self.grNode = RAPMACGraphicsNode(self)
        self.content.expression.textChanged.connect(self.onInputChanged)

    def get_code_string(self):
        return self.content.expression.text() + ";"

    def evalImplementation(self):
        pass

######################################################################
############################## Variable ##############################
######################################################################

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
    node_type = NODE_TYPE_NORMAL

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[1])
        self.eval()

    def initInnerClasses(self):
        self.content = RAPMAC_Variable_Content(self)
        self.grNode = RAPMAC_Variable_GraphicsNode(self)
        self.content.expression.textChanged.connect(self.onInputChanged)
        self.content.variable_name.textChanged.connect(self.onInputChanged)

    def get_code_string(self):
        return self.content.expression.text() + " " + self.content.variable_name.text() + ";"

    def evalImplementation(self):
        pass