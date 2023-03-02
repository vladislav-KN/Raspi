import os
import time
from threading import Thread

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from src.controlls.save_loader import SaveLoad


class Element(QWidget):
    def __init__(self, cost="50 рублей", name="Водичка", file="1", parent=None):
        super(Element, self).__init__(parent)
        self.setMinimumSize(QSize(250, 373))
        self.setMaximumSize(QSize(250, 373))
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.frmMain = QFrame(self)
        self.frmMain.setEnabled(True)
        self.frmMain.setMinimumSize(QSize(250, 373))
        self.frmMain.setMaximumSize(QSize(250, 373))
        self.frmMain.setStyleSheet("background-color: rgb(246, 246, 246);")
        self.frmMain.setFrameShape(QFrame.StyledPanel)
        self.frmMain.setFrameShadow(QFrame.Raised)
        self.frmMain.setObjectName("frmMain")
        self.gridLayout_46 = QGridLayout(self.frmMain)
        self.gridLayout_46.setObjectName("gridLayout_46")
        self.grdMain = QGridLayout()
        self.grdMain.setObjectName("grdMain")
        self.lbCost = QLabel(self.frmMain)
        self.lbCost.setObjectName("lbCost")
        self.grdMain.addWidget(self.lbCost, 1, 1, 1, 1)
        self.lbName = QLabel(self.frmMain)
        self.lbName.setObjectName("lbName")
        self.grdMain.addWidget(self.lbName, 1, 0, 1, 1)
        self.frame_qr = QFrame(self.frmMain)
        self.frame_qr.setMinimumSize(QSize(123, 123))
        self.frame_qr.setMaximumSize(QSize(123, 123))
        self.frame_qr.setStyleSheet(f"image: url(src/res/imgs/{file}/qr.png);")
        self.frame_qr.setFrameShape(QFrame.StyledPanel)
        self.frame_qr.setFrameShadow(QFrame.Raised)
        self.frame_qr.setObjectName("frame_qr")
        self.grdMain.addWidget(self.frame_qr, 2, 0, 1, 2)
        self.frame_img = QFrame(self.frmMain)
        self.frame_img.setMinimumSize(QSize(200, 200))
        self.frame_img.setMaximumSize(QSize(200, 200))
        self.frame_img.setContextMenuPolicy(Qt.CustomContextMenu)
        self.frame_img.setToolTipDuration(-1)
        self.frame_img.setStyleSheet(f"image: url(src/res/imgs/{file}/img.png);")
        self.frame_img.setFrameShape(QFrame.StyledPanel)
        self.frame_img.setFrameShadow(QFrame.Raised)
        self.frame_img.setObjectName("frame_img")
        _translate = QCoreApplication.translate
        self.lbCost.setText(_translate("MainWindow", cost))
        self.lbName.setText(_translate("MainWindow", name))
        self.grdMain.addWidget(self.frame_img, 0, 0, 1, 2)
        self.gridLayout_46.addLayout(self.grdMain, 0, 0, 1, 1)


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setObjectName("MainWindow")
        self.setStyleSheet("background-color: rgb(47, 66, 115);")
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 1038, 1151))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_3 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout_3.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout.addWidget(self.scrollArea)
        self.vscrollbar = self.scrollArea.verticalScrollBar()
        self.showFullScreen()
        self.curid = (0, 0)
        self.maxid_w = 0

    def load(self, file):
        self.update()
        QApplication.processEvents()
        self.maxid_w = self.width() // 250 - 1
        for item in SaveLoad(file).load_from_file()["elem"]:
            self.addElmToGrid(Element(file=item["folder"], name=item["name"], cost=item["price"]))
            self.update()
            QApplication.processEvents()

    def addElmToGrid(self, elem):
        if self.curid[1] == self.maxid_w:
            self.curid = (self.curid[0] + 1, 0)
        self.gridLayout.addWidget(elem, self.curid[0], self.curid[1], 1, 1)
        self.curid = (self.curid[0], self.curid[1] + 1)

    def scrole(self):
        while True:
            try:
                time.sleep(5)
                for i in range(1, self.gridLayout.rowCount()):
                    self.animate((i - 1) * 384, i * 384, 5, 5)
                for i in range(self.gridLayout.rowCount(), 0, -1):
                    self.animate(i * 384, (i-1) * 384, -5, 3)
            except:
                break

    def animate(self, _from: int, _to: int, step=1, pause=5.0):
        if step == 0: return
        if (step > 0):
            x = lambda a, b: a <= b
        else:
            x = lambda a, b: a >= b

        while (x(_from, _to)):
            self.vscrollbar.setValue(_from)
            _from += step
            time.sleep(1 / 60)
        time.sleep(pause)


def main():
    app = QApplication([])
    ex = MainWindow()
    ex.load("../data/gui.json")
    def func():
        ex.scrole()
        while (True):
            if os.path.exists("close"):
                app.exit()
                os.remove("close")
                break

    t = Thread(target=func)
    t.start()
    app.exec()
    return


if __name__ == '__main__':
    proc = Thread(target=main)
    proc.start()
