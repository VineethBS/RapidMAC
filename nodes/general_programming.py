from PyQt5.QtCore import *
from rapidmac_conf import *
from rapidmac_node_base import *
from nodeeditor.utils import dumpException
######################################################################
############################### If ###################################
######################################################################
class RAPMAC_If_Dialog(QDialog):
    def __init__(self, parent = None):
        super(RAPMAC_If_Dialog, self).__init__(parent)
        
        self.parent = parent

        self.setWindowTitle("If")
        
        self.if_if = QLabel("if ", self)
        self.if_start = QLabel("{")
        self.if_end = QLabel("}")

        self.if_condition = QLineEdit(self)
        self.if_body = QPlainTextEdit(self)
        
        self.if_condition.setText(self.parent.if_condition)
        self.if_body.setPlainText(self.parent.if_body)
        self.if_body.setStyleSheet("color:white")

        gridlayout = QGridLayout()
        gridlayout.addWidget(self.if_if, 0, 0, 1, 1)
        gridlayout.addWidget(self.if_condition, 0, 1, 1, 1)
        gridlayout.addWidget(self.if_start,1,0,1,1)
        gridlayout.addWidget(self.if_body,2,0,3,2)
        gridlayout.addWidget(self.if_end, 5, 0, 1, 1)
        
        qbtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        buttonbox = QDialogButtonBox(qbtn)
        buttonbox.accepted.connect(self.accept)
        buttonbox.rejected.connect(self.reject)
        
        layout = QVBoxLayout()
        layout.addLayout(gridlayout)
        layout.addWidget(buttonbox)
        
        self.setLayout(layout)

    def accept(self):
        self.done(self.Accepted)
        self.parent.if_condition = self.if_condition.text()
        self.parent.if_body = self.if_body.toPlainText()

class RAPMAC_If_Content(QDMNodeContentWidget):
    def initUI(self):
        self.if_condition = ""
        self.if_body = ""

        self.label = QLabel(self)
        self.label.setWordWrap(True)
        self.label.setText("if (" + self.if_condition + ")")
        self.edit = QPushButton("Edit ...", self)
        self.edit.setObjectName(self.node.content_label_objname)
        self.edit.clicked.connect(self.onEditButtonClick)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.edit)
        self.setLayout(layout)

    def onEditButtonClick(self, s):
        dlg = RAPMAC_If_Dialog(self) 
        dlg.exec_()
        self.label.setText("if (" + self.if_condition + ")")
        
    def serialize(self):
        res = super().serialize()
        res['if_condition'] = self.if_condition
        res['if_body'] = self.if_body
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        try:
            self.if_condition = data['if_condition']
            self.if_body = data['if_body']
            return True & res
        except Exception as e:
            dumpException(e)
        return res

@register_node(OP_NODE_IF)
class RAPMACNode_If(RAPMACNode):
    icon = "icons/in.png"
    op_code = OP_NODE_IF
    op_title = "If"
    node_type = NODE_TYPE_NORMAL
    content_label_objname = "node_if"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[1])
        self.eval()

    def initInnerClasses(self):
        self.content = RAPMAC_If_Content(self)
        self.grNode = RAPMACGraphicsNode(self)
        self.grNode.width = 160
        self.grNode.height = 100

    def get_code_string(self):
        return "if (" + self.content.if_condition + ") \n {" + self.content.if_body + "}\n"

    def evalImplementation(self):
        pass


######################################################################
############################ For loop ################################
######################################################################
class RAPMAC_For_Dialog(QDialog):
    def __init__(self, parent = None):
        super(RAPMAC_For_Dialog, self).__init__(parent)
        
        self.parent = parent

        self.setWindowTitle("For loop")
        
        self.for_for = QLabel("for ", self)
        self.for_start = QLabel("{")
        self.for_end = QLabel("}")

        self.for_condition = QLineEdit(self)
        self.for_body = QPlainTextEdit(self)
        
        self.for_condition.setText(self.parent.for_condition)
        self.for_body.setPlainText(self.parent.for_body)
        self.for_body.setStyleSheet("color:white")

        gridlayout = QGridLayout()
        gridlayout.addWidget(self.for_for, 0, 0, 1, 1)
        gridlayout.addWidget(self.for_condition, 0, 1, 1, 1)
        gridlayout.addWidget(self.for_start,1,0,1,1)
        gridlayout.addWidget(self.for_body,2,0,3,2)
        gridlayout.addWidget(self.for_end, 5, 0, 1, 1)
        
        qbtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        buttonbox = QDialogButtonBox(qbtn)
        buttonbox.accepted.connect(self.accept)
        buttonbox.rejected.connect(self.reject)
        
        layout = QVBoxLayout()
        layout.addLayout(gridlayout)
        layout.addWidget(buttonbox)
        
        self.setLayout(layout)

    def accept(self):
        self.done(self.Accepted)
        self.parent.for_condition = self.for_condition.text()
        self.parent.for_body = self.for_body.toPlainText()

class RAPMAC_For_Content(QDMNodeContentWidget):
    def initUI(self):
        self.for_condition = ""
        self.for_body = ""

        self.label = QLabel(self)
        self.label.setWordWrap(True)
        self.label.setText("for (" + self.for_condition + ")")
        self.edit = QPushButton("Edit ...", self)
        self.edit.setObjectName(self.node.content_label_objname)
        self.edit.clicked.connect(self.onEditButtonClick)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.edit)
        self.setLayout(layout)

    def onEditButtonClick(self, s):
        dlg = RAPMAC_For_Dialog(self) 
        dlg.exec_()
        self.label.setText("for (" + self.for_condition + ")")
        
    def serialize(self):
        res = super().serialize()
        res['for_condition'] = self.for_condition
        res['for_body'] = self.for_body
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        try:
            self.for_condition = data['for_condition']
            self.for_body = data['for_body']
            return True & res
        except Exception as e:
            dumpException(e)
        return res

@register_node(OP_NODE_FOR)
class RAPMACNode_For(RAPMACNode):
    icon = "icons/in.png"
    op_code = OP_NODE_FOR
    op_title = "For loop"
    node_type = NODE_TYPE_NORMAL
    content_label_objname = "node_for"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[1])
        self.eval()

    def initInnerClasses(self):
        self.content = RAPMAC_For_Content(self)
        self.grNode = RAPMACGraphicsNode(self)
        self.grNode.width = 160
        self.grNode.height = 100

    def get_code_string(self):
        return "for (" + self.content.for_condition + ") \n {" + self.content.for_body + "}\n"

    def evalImplementation(self):
        pass


######################################################################
########################## While loop ################################
######################################################################
class RAPMAC_While_Dialog(QDialog):
    def __init__(self, parent = None):
        super(RAPMAC_While_Dialog, self).__init__(parent)
        
        self.parent = parent

        self.setWindowTitle("While loop")
        
        self.while_while = QLabel("while ", self)
        self.while_start = QLabel("{")
        self.while_end = QLabel("}")

        self.while_condition = QLineEdit(self)
        self.while_body = QPlainTextEdit(self)
        
        self.while_condition.setText(self.parent.while_condition)
        self.while_body.setPlainText(self.parent.while_body)
        self.while_body.setStyleSheet("color:white")

        gridlayout = QGridLayout()
        gridlayout.addWidget(self.while_while, 0, 0, 1, 1)
        gridlayout.addWidget(self.while_condition, 0, 1, 1, 1)
        gridlayout.addWidget(self.while_start,1,0,1,1)
        gridlayout.addWidget(self.while_body,2,0,3,2)
        gridlayout.addWidget(self.while_end, 5, 0, 1, 1)
        
        qbtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        buttonbox = QDialogButtonBox(qbtn)
        buttonbox.accepted.connect(self.accept)
        buttonbox.rejected.connect(self.reject)
        
        layout = QVBoxLayout()
        layout.addLayout(gridlayout)
        layout.addWidget(buttonbox)
        
        self.setLayout(layout)

    def accept(self):
        self.done(self.Accepted)
        self.parent.while_condition = self.while_condition.text()
        self.parent.while_body = self.while_body.toPlainText()

class RAPMAC_While_Content(QDMNodeContentWidget):
    def initUI(self):
        self.while_condition = ""
        self.while_body = ""

        self.label = QLabel(self)
        self.label.setWordWrap(True)
        self.label.setText("while (" + self.while_condition + ")")
        self.edit = QPushButton("Edit ...", self)
        self.edit.setObjectName(self.node.content_label_objname)
        self.edit.clicked.connect(self.onEditButtonClick)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.edit)
        self.setLayout(layout)

    def onEditButtonClick(self, s):
        dlg = RAPMAC_While_Dialog(self) 
        dlg.exec_()
        self.label.setText("while (" + self.while_condition + ")")
        
    def serialize(self):
        res = super().serialize()
        res['while_condition'] = self.while_condition
        res['while_body'] = self.while_body
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        try:
            self.while_condition = data['while_condition']
            self.while_body = data['while_body']
            return True & res
        except Exception as e:
            dumpException(e)
        return res

@register_node(OP_NODE_WHILE)
class RAPMACNode_While(RAPMACNode):
    icon = "icons/in.png"
    op_code = OP_NODE_WHILE
    op_title = "While loop"
    node_type = NODE_TYPE_NORMAL
    content_label_objname = "node_while"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[1])
        self.eval()

    def initInnerClasses(self):
        self.content = RAPMAC_While_Content(self)
        self.grNode = RAPMACGraphicsNode(self)
        self.grNode.width = 160
        self.grNode.height = 100

    def get_code_string(self):
        return "while (" + self.content.while_condition + ") \n {" + self.content.while_body + "}\n"

    def evalImplementation(self):
        pass

######################################################################
##################### Preprocessor #INCLUDE ##########################
######################################################################
# TODO - all classes - code generation can be moved into the content class
class RAPMAC_HashInclude_Content(QDMNodeContentWidget):
    def initUI(self):
        self.expression = QLineEdit("", self)
        self.expression.width = 100
        self.expression.setAlignment(Qt.AlignLeft)
        self.expression.setObjectName(self.node.content_label_objname)

        self.usequotes = QRadioButton("Use \" \"")
        self.usequotes.setStyleSheet("color:yellow")
        self.useangular = QRadioButton("Use < > ")
        self.useangular.setStyleSheet("color:yellow")

        gridlayout = QGridLayout()
        gridlayout.addWidget(self.expression, 0, 0, 1, 2)
        gridlayout.addWidget(self.usequotes, 1, 0, 1, 1)
        gridlayout.addWidget(self.useangular, 1, 1, 1, 1)
        self.setLayout(gridlayout)

    def serialize(self):
        res = super().serialize()
        res['expression'] = self.expression.text()
        res['usequotes'] = self.usequotes.isChecked()
        res['useangular'] = self.useangular.isChecked()
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        try:
            value = data['expression']
            self.expression.setText(value)
            if data['usequotes']:
                self.usequotes.setChecked()
            if data['useangular']:
                self.useangular.setChecked()
            return True & res
        except Exception as e:
            dumpException(e)
        return res

@register_node(OP_NODE_INCLUDE)
class RAPMACNode_Include(RAPMACNode):
    icon = "icons/in.png"
    op_code = OP_NODE_INCLUDE
    op_title = "# INCLUDE"
    node_type = NODE_TYPE_NORMAL
    content_label_objname = "node_hash_include"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[1])
        self.eval()

    def initInnerClasses(self):
        self.content = RAPMAC_HashInclude_Content(self)
        self.grNode = RAPMACGraphicsNode(self)
        self.grNode.width = 160
        self.grNode.height = 100

    def get_code_string(self):
        if self.content.useangular.isChecked():
            return "#INCLUDE <" + self.content.expression.text() + ">"
        if self.content.usequotes.isChecked():
            return "#INCLUDE \"" + self.content.expression.text() + "\""

    def evalImplementation(self):
        pass

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
class RAPMACNode_Define(RAPMACNode):
    icon = "icons/in.png"
    op_code = OP_NODE_DEFINE
    op_title = "# DEFINE"
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
        self.label.width = 140
        self.label.height = 90
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

    def initInnerClasses(self):
        self.content = RAPMAC_Comment_Content(self)
        self.grNode = RAPMACGraphicsNode(self)
        self.grNode.width = 160
        self.grNode.height = 120

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