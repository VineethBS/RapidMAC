LISTBOX_MIMETYPE = "application/x-item"

NODE_TYPE_START = 1
NODE_TYPE_CONTAINER = 2
NODE_TYPE_NORMAL = 3

MAX_NODES_PER_CATEGORY = 99

OP_MAC_NODES_START = 100
OP_NODE_INIT = OP_MAC_NODES_START + 1
OP_NODE_SEND_PACKET = OP_MAC_NODES_START + 2
OP_NODE_PACKET_INPUT = OP_MAC_NODES_START + 3
OP_NODE_ON = OP_MAC_NODES_START + 4
OP_NODE_OFF = OP_MAC_NODES_START + 5
OP_NODE_CCI = OP_MAC_NODES_START + 6

OP_CSRC_NODES_START = 200
OP_NODE_HEADER = OP_CSRC_NODES_START + 1
OP_NODE_MACRO = OP_CSRC_NODES_START + 2
OP_NODE_VARIABLE = OP_CSRC_NODES_START + 3
OP_NODE_EXPRESSION = OP_CSRC_NODES_START + 4
OP_NODE_MULTILINEEXPRESSION = OP_CSRC_NODES_START + 5
OP_NODE_COMMENT = OP_CSRC_NODES_START + 6
OP_NODE_FUNCTION_DECLARATION = OP_CSRC_NODES_START + 7
OP_NODE_FUNCTION_DEFINITION = OP_CSRC_NODES_START + 8
OP_NODE_FUNCTION_CALL = OP_CSRC_NODES_START + 9

RAPMAC_NODES = {}


class ConfException(Exception): pass
class InvalidNodeRegistration(ConfException): pass
class OpCodeNotRegistered(ConfException): pass


def register_node_now(op_code, class_reference):
    if op_code in RAPMAC_NODES:
        raise InvalidNodeRegistration("Duplicate node registration of '%s'. There is already %s" %(
            op_code, RAPMAC_NODES[op_code]
        ))
    RAPMAC_NODES[op_code] = class_reference


def register_node(op_code):
    def decorator(original_class):
        register_node_now(op_code, original_class)
        return original_class
    return decorator

def get_class_from_opcode(op_code):
    if op_code not in RAPMAC_NODES: raise OpCodeNotRegistered("OpCode '%d' is not registered" % op_code)
    return RAPMAC_NODES[op_code]

# import all nodes and register them
from nodes import *