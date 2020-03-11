import os
import sys
from PyQt5.QtWidgets import *

from rapidmac_window import RapidMACWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # print(QStyleFactory.keys())
    # app.setStyle('Windows')
    app.setStyle('Fusion')

    wnd = RapidMACWindow()
    wnd.show()

    sys.exit(app.exec_())
