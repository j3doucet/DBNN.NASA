
#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
ZetCode PySide tutorial 

This example draws three rectangles in three
different colors. 

author: Jan Bodnar
website: zetcode.com 
last edited: August 2011
"""

import sys
from math import exp
from PySide import QtGui, QtCore

class Example(QtGui.QWidget):
    
    def __init__(self,container):
        super(Example, self).__init__(container)
        self.setParent(container)
        self.initUI()
        
    def initUI(self):      

        self.setGeometry(300, 300, 280, 270)
        #self.setWindowTitle('Brain')
        #self.show()
        print "hello instatiated"
        #print dir(self)
        self.show()


    def paintEvent(self, e):

        qp = QtGui.QPainter()
        qp.begin(self)
        print "hello painted" 
        xinit = 30
        yinit = 30

        for i in range(1,9):
            for j in range(1,9):
                self.ConnectNodes(qp,xinit, yinit+i*40, xinit+40, yinit+i*40, 1) 
            self.drawNode(qp,xinit, yinit+i*40)

        self.drawLines(qp)
        qp.end()

    def drawNode(self, qp, x, y):
        pen = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine)
        gradient = QtGui.QRadialGradient(50, 50, 50, 50, 50)
        gradient.setColorAt(0, QtGui.QColor.fromRgbF(0, 1, 0, 1))
        gradient.setColorAt(1, QtGui.QColor.fromRgbF(0, 0, 0, 0))
        qp.setBrush(gradient)

        qp.setPen(pen)
        qp.drawEllipse(QtCore.QPointF(x,y),20,20);

    
    def ConnectNodes(self, qp, x1, y1, x2, y2, w):
        pen = QtGui.QPen(QtCore.Qt.black, 8*1.0/(1.0+exp(-w)), QtCore.Qt.SolidLine)
        qp.setPen(pen)

        qp.drawLine(x1,y1,x2,y2)


def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
