
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

import time
import sys
import random
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
        for t in range(1,10):
            xinit = 30
            yinit = 30
            xspace = 150
            yspace = 60
            for i in range(1,9):
                for j in range(1,9):
                    self.ConnectNodes(qp,xinit, yinit+i*yspace, xinit+xspace, yinit+j*yspace, 0) 
                self.drawNode(qp,xinit, yinit+i*yspace, 0)

            xinit = xinit + xspace 
            for i in range(1,9):
                for j in range(2,8):
                    self.ConnectNodes(qp,xinit, yinit+i*yspace, xinit+xspace, yinit+j*yspace, 0) 
                self.drawNode(qp,xinit, yinit+i*yspace, 0)

            xinit = xinit + xspace
            for i in range(2,8):
                for j in range(3,8):
                    self.ConnectNodes(qp,xinit, yinit+i*yspace, xinit+xspace, yinit+j*yspace-yspace/2, 0) 
                self.drawNode(qp,xinit, yinit+i*yspace, 0)

            xinit = xinit + xspace
            for i in range(2,7):
                self.drawNode(qp,xinit, yinit+i*yspace + yspace/2, 1)
        qp.end()

    def drawNode(self, qp, x, y, isend):
        pen = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine)
        gradient = QtGui.QRadialGradient(x, y, 20, x,y)
        if(random.random() < 0.25):
            gradient.setColorAt(0, QtGui.QColor.fromRgbF(0, 1, 0, 1))
        else:
            gradient.setColorAt(0, QtGui.QColor.fromRgbF(1, 0, 0, 1))
        if(isend == 1):
            gradient.setColorAt(0, QtGui.QColor.fromRgbF(0, 0, random.random(),1))


        gradient.setColorAt(1, QtGui.QColor.fromRgbF(0, 0, 0, 0.8))
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
