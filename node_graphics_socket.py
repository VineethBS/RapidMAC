from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class QDMGraphicsSocket(QGraphicsItem):
    def __init__(self, socket,socket_type=1):
##        print('*----node_graphics_socket----*')
        self.socket = socket
        super().__init__(socket.node.grNode)

        self.radius = 6.0
        self.outline_width = 1.0
        self._colors = [QColor("#FAFE7700"),QColor("#FBF52e22"),
                        QColor("#FCFE4700"),QColor("#FEFE7700"),
                        QColor("#FDbE7700"),QColor("#FF3E77c0")]
        self._color_background = self._colors[socket_type]
        self._color_outline = QColor("#FF000000")           

        self._pen = QPen(self._color_outline)
        self._pen.setWidthF(self.outline_width)
        self._brush = QBrush(self._color_background)

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
##        print('*----node_graphics_socket--(paint)--*')
        # painting circle
        painter.setBrush(self._brush)
        painter.setPen(self._pen)
        painter.drawEllipse(-self.radius, -self.radius, 2 * self.radius, 2 * self.radius)

    def boundingRect(self):
#        print('*----node_graphics_socket-(boundingRect)---*')
        return QRectF(
            - self.radius - self.outline_width,
            - self.radius - self.outline_width,
            2 * (self.radius + self.outline_width),
            2 * (self.radius + self.outline_width),
        )


