import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

"""
Q: 如何使用PyQt实现一个进度条
pip install PyQt5
"""


class UiDialog(object):

    def __init__(self):
        self.label = QLabel()
        self.pBar = QProgressBar()

    def setup(self, dialog):
        if not dialog.objectName():
            dialog.setObjectName(u"Dialog")
        dialog.resize(270, 119)
        dialog.setMinimumSize(QSize(270, 119))
        dialog.setMaximumSize(QSize(270, 119))
        self.label = QLabel(dialog)
        self.pBar = QProgressBar(dialog)
        self.pBar.setGeometry(QRect(20, 50, 261, 41))
        self.pBar.setMaximum(0)
        self.pBar.setMinimum(0)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, 20, 141, 21))
        self.retranslate(dialog)
        QMetaObject.connectSlotsByName(dialog)

    def retranslate(self, dialog):
        dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Massage", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p>"
                                                                u"<span style=\" font-size:11pt; "
                                                                u"font-weight:600"
                                                                u";\">\u7cfb\u7edf\u7e41\u5fd9\u4e2d\u3002\u3002\u3002"
                                                                u"</span></p></body></html>", None))


class MyDialog(QDialog, UiDialog):
    def __init__(self, parent=None):
        super(MyDialog, self).__init__(parent)
        self.setup(self)

    def closeEvent(self, event):
        """
        PS: 重写关闭事件，注意此函数名不可变
        """
        message_box = QMessageBox(self)
        reply = message_box.question(self, u'警告', u'确认退出?', QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyDialog()
    """
    Q: 如何实现无边框的进度条
    A: ex.setWindowFlags(Qt.FramelessWindowHint)
    """
    ex.show()
    sys.exit(app.exec_())
