from PyQt5.QtCore import *
from rapidmac_conf import *
from rapidmac_node_base import *
from nodeeditor.utils import dumpException
######################################################################
########################## Function call #############################
######################################################################
class RAPMAC_FunctionCall_Dialog(QDialog):
    def __init__(self, parent = None):
        super(RAPMAC_FunctionCall_Dialog, self).__init__(parent)
        
        self.parent = parent

        self.setWindowTitle("Edit function call")
        
        self.function_name_l = QLabel("Function name", self)
        self.function_arguments_l = QLabel("Argument list (type and name)", self)
        
        self.function_name_e = QLineEdit(self)
        self.function_arguments_e = QLineEdit(self)
        
        self.function_name_e.setText(self.parent.function_name)
        self.function_arguments_e.setText(self.parent.function_arguments)
        
        gridlayout = QGridLayout()
        gridlayout.addWidget(self.function_name_l, 0, 0, 1, 1)
        gridlayout.addWidget(self.function_name_e, 0, 1, 1, 1)
        gridlayout.addWidget(self.function_arguments_l, 3, 0, 1, 1)
        gridlayout.addWidget(self.function_arguments_e, 3, 1, 1, 1)
        
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
        self.parent.function_name = self.function_name_e.text()
        self.parent.function_arguments = self.function_arguments_e.text()
        
class RAPMAC_FunctionCall_Content(QDMNodeContentWidget):
    def initUI(self):
        self.function_name = ""
        self.function_arguments = ""
        
        self.label = QLabel(self)
        self.label.setWordWrap(True)
        self.label.setText(self.function_name + "(" + self.function_arguments + ")")
        self.edit = QPushButton("Edit ...", self)
        self.edit.setObjectName(self.node.content_label_objname)
        self.edit.clicked.connect(self.onEditButtonClick)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.edit)
        self.setLayout(layout)

    def onEditButtonClick(self, s):
        dlg = RAPMAC_FunctionCall_Dialog(self) 
        dlg.exec_()
        self.label.setText(self.function_name + "(" + self.function_arguments + ")")
        
    def serialize(self):
        res = super().serialize()
        res['function_name'] = self.function_name
        res['function_arguments'] = self.function_arguments
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        try:
            self.function_name = data['function_name']
            self.function_arguments = data['function_arguments']
            return True & res
        except Exception as e:
            dumpException(e)
        return res

@register_node(OP_NODE_FUNCTION_CALL)
class RAPMACNode_FunctionCall(RAPMACNode):
    icon = "icons/in.png"
    op_code = OP_NODE_FUNCTION_CALL
    op_title = "Function call"
    node_type = NODE_TYPE_NORMAL
    content_label_objname = "node_function_call"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[1])
        self.eval()

    def initInnerClasses(self):
        self.content = RAPMAC_FunctionCall_Content(self)
        self.grNode = RAPMACGraphicsNode(self)

    def get_code_string(self):
        return self.content.function_name + " (" + self.content.function_arguments + ");\n"

    def evalImplementation(self):
        pass
######################################################################
###################### Function Definition ###########################
######################################################################
class RAPMAC_FunctionDefinition_Dialog(QDialog):
    def __init__(self, parent = None):
        super(RAPMAC_FunctionDefinition_Dialog, self).__init__(parent)
        
        self.parent = parent

        self.setWindowTitle("Edit function definition")
        
        self.function_name_l = QLabel("Function name", self)
        self.function_type_l = QLabel("Function type (extern/static)", self)
        self.function_return_type_l = QLabel("Return type", self)
        self.function_arguments_l = QLabel("Argument list (type and name)", self)
        self.function_start = QLabel("{")
        self.function_end = QLabel("}")

        self.function_name_e = QLineEdit(self)
        self.function_type_e = QLineEdit(self)
        self.function_return_type_e = QLineEdit(self)
        self.function_arguments_e = QLineEdit(self)
        self.function_body_e = QPlainTextEdit(self)
        
        self.function_name_e.setText(self.parent.function_name)
        self.function_type_e.setText(self.parent.function_type)
        self.function_return_type_e.setText(self.parent.function_return_type)
        self.function_arguments_e.setText(self.parent.function_arguments)
        self.function_body_e.setPlainText(self.parent.function_body)
        self.function_body_e.setStyleSheet("color:white")

        gridlayout = QGridLayout()
        gridlayout.addWidget(self.function_name_l, 0, 0, 1, 1)
        gridlayout.addWidget(self.function_name_e, 0, 1, 1, 1)
        gridlayout.addWidget(self.function_type_l, 1, 0, 1, 1)
        gridlayout.addWidget(self.function_type_e, 1, 1, 1, 1)
        gridlayout.addWidget(self.function_return_type_l, 2, 0, 1, 1)
        gridlayout.addWidget(self.function_return_type_e, 2, 1, 1, 1)
        gridlayout.addWidget(self.function_arguments_l, 3, 0, 1, 1)
        gridlayout.addWidget(self.function_arguments_e, 3, 1, 1, 1)
        gridlayout.addWidget(self.function_start,4,0,1,1)
        gridlayout.addWidget(self.function_body_e,5,0,3,2)
        gridlayout.addWidget(self.function_end, 8, 0, 1, 1)
        

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
        self.parent.function_name = self.function_name_e.text()
        self.parent.function_type = self.function_type_e.text()
        self.parent.function_return_type = self.function_return_type_e.text()
        self.parent.function_arguments = self.function_arguments_e.text()
        self.parent.function_body = self.function_body_e.toPlainText()

class RAPMAC_FunctionDefinition_Content(QDMNodeContentWidget):
    def initUI(self):
        self.function_name = ""
        self.function_type = ""
        self.function_return_type = ""
        self.function_arguments = ""
        self.function_body = ""

        self.label = QLabel(self)
        self.label.setWordWrap(True)
        self.label.setText(self.function_name)
        self.edit = QPushButton("Edit ...", self)
        self.edit.setObjectName(self.node.content_label_objname)
        self.edit.clicked.connect(self.onEditButtonClick)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.edit)
        self.setLayout(layout)

    def onEditButtonClick(self, s):
        dlg = RAPMAC_FunctionDefinition_Dialog(self) 
        dlg.exec_()
        self.label.setText(self.function_name)
        
    def serialize(self):
        res = super().serialize()
        res['function_name'] = self.function_name
        res['function_type'] = self.function_type
        res['function_return_type'] = self.function_return_type
        res['function_arguments'] = self.function_arguments
        res['function_body'] = self.function_body
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        try:
            self.function_name = data['function_name']
            self.function_type = data['function_type']
            self.function_return_type = data['function_return_type']
            self.function_arguments = data['function_arguments']
            self.function_body = data['function_body']
            return True & res
        except Exception as e:
            dumpException(e)
        return res

@register_node(OP_NODE_FUNCTION_DEFINITION)
class RAPMACNode_FunctionDefinition(RAPMACNode):
    icon = "icons/in.png"
    op_code = OP_NODE_FUNCTION_DEFINITION
    op_title = "Function definition"
    node_type = NODE_TYPE_NORMAL
    content_label_objname = "node_function_definition"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[1])
        self.eval()

    def initInnerClasses(self):
        self.content = RAPMAC_FunctionDefinition_Content(self)
        self.grNode = RAPMACGraphicsNode(self)

    def get_code_string(self):
        return self.content.function_type + " " + self.content.function_return_type + " " + \
            self.content.function_name + " (" + \
            self.content.function_arguments + ");\n" + "{\n" + \
            self.content.function_body + "\n}\n"

    def evalImplementation(self):
        pass

######################################################################
###################### Function Declaration ##########################
######################################################################
class RAPMAC_FunctionDeclaration_Dialog(QDialog):
    def __init__(self, parent = None):
        super(RAPMAC_FunctionDeclaration_Dialog, self).__init__(parent)
        
        self.parent = parent

        self.setWindowTitle("Edit function declaration")
        
        self.function_name_l = QLabel("Function name", self)
        self.function_type_l = QLabel("Function type (extern/static)", self)
        self.function_return_type_l = QLabel("Return type", self)
        self.function_arguments_l = QLabel("Argument list (type and name)", self)

        self.function_name_e = QLineEdit(self)
        self.function_type_e = QLineEdit(self)
        self.function_return_type_e = QLineEdit(self)
        self.function_arguments_e = QLineEdit(self)
        
        self.function_name_e.setText(self.parent.function_name)
        self.function_type_e.setText(self.parent.function_type)
        self.function_return_type_e.setText(self.parent.function_return_type)
        self.function_arguments_e.setText(self.parent.function_arguments)
        
        gridlayout = QGridLayout()
        gridlayout.addWidget(self.function_name_l, 0, 0, 1, 1)
        gridlayout.addWidget(self.function_name_e, 0, 1, 1, 1)
        gridlayout.addWidget(self.function_type_l, 1, 0, 1, 1)
        gridlayout.addWidget(self.function_type_e, 1, 1, 1, 1)
        gridlayout.addWidget(self.function_return_type_l, 2, 0, 1, 1)
        gridlayout.addWidget(self.function_return_type_e, 2, 1, 1, 1)
        gridlayout.addWidget(self.function_arguments_l, 3, 0, 1, 1)
        gridlayout.addWidget(self.function_arguments_e, 3, 1, 1, 1)
        

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
        self.parent.function_name = self.function_name_e.text()
        self.parent.function_type = self.function_type_e.text()
        self.parent.function_return_type = self.function_return_type_e.text()
        self.parent.function_arguments = self.function_arguments_e.text()

class RAPMAC_FunctionDeclaration_Content(QDMNodeContentWidget):
    def initUI(self):
        self.function_name = ""
        self.function_type = ""
        self.function_return_type = ""
        self.function_arguments = ""

        self.label = QLabel(self)
        self.label.setWordWrap(True)
        self.label.setText(self.function_name)
        self.edit = QPushButton("Edit ...", self)
        self.edit.setObjectName(self.node.content_label_objname)
        self.edit.clicked.connect(self.onEditButtonClick)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.edit)
        self.setLayout(layout)

    def onEditButtonClick(self, s):
        dlg = RAPMAC_FunctionDeclaration_Dialog(self) 
        dlg.exec_()
        self.label.setText(self.function_name)
        
    def serialize(self):
        res = super().serialize()
        res['function_name'] = self.function_name
        res['function_type'] = self.function_type
        res['function_return_type'] = self.function_return_type
        res['function_arguments'] = self.function_arguments
        return res

    def deserialize(self, data, hashmap={}):
        res = super().deserialize(data, hashmap)
        try:
            self.function_name = data['function_name']
            self.function_type = data['function_type']
            self.function_return_type = data['function_return_type']
            self.function_arguments = data['function_arguments']
            return True & res
        except Exception as e:
            dumpException(e)
        return res

@register_node(OP_NODE_FUNCTION_DECLARATION)
class RAPMACNode_FunctionDeclaration(RAPMACNode):
    icon = "icons/in.png"
    op_code = OP_NODE_FUNCTION_DECLARATION
    op_title = "Function declaration"
    node_type = NODE_TYPE_NORMAL
    content_label_objname = "node_function_declaration"

    def __init__(self, scene):
        super().__init__(scene, inputs=[1], outputs=[1])
        self.eval()

    def initInnerClasses(self):
        self.content = RAPMAC_FunctionDeclaration_Content(self)
        self.grNode = RAPMACGraphicsNode(self)

    def get_code_string(self):
        return self.content.function_type + " " + self.content.function_return_type + " " + \
            self.content.function_name + " (" + self.content.function_arguments + ");\n"

    def evalImplementation(self):
        pass
