
#!/usr/bin/python
# -*- coding: utf-8 -*-


import time
import threading
import sys
import random
import re
from math import exp
from PySide import QtGui, QtCore
import sys

class Example(QtGui.QWidget):

    def getWeights(pythonisdumbdumb,x):
        f = open("./../Data/Model.NN","r")
        lines = f.readlines();

        matrices = []
        matrix = []
        for line in lines:
            row = []
            result = re.match("(\d+)\s+(\d+)\s*\n", line)
            if(result):
                #rows = result.group[0] 
                #cols = result.group[1]
                if(len(matrix) != 0):
                    matrices.append(matrix)
                    matrix = []
            else:
                row = line.split()
                matrix.append(row)
        matrices.append(matrix)
        return matrices[x]


    lock = threading.Lock()
    currentData = [-10, -5, 5, 10, -1, 0, 0, 1]
    def getData(self, tehdataz):
        yield from lock
        try:
            self.currentData = tehdataz
        finally:
            lock.release()

    def __init__(self):
        super(Example, self).__init__()

        self.initUI()

    def initUI(self):      

        print("hello\n")
        sys.stdout.flush
        self.setGeometry(300, 300, 280, 270)
        self.setWindowTitle('Brain')
        self.show()
        print("hello\n")
        sys.stdout.flush


    def paintEvent(self, e):
        print("hello\n")
        sys.stdout.flush

        qp = QtGui.QPainter()
        qp.begin(self)

        for t in range(1,10):
            xinit = 30
            yinit = 30
            xspace = 150
            yspace = 60
            matrix = self.getWeights(1)
            mysum = []
            print("hello\n")
            sys.stdout.flush

            for i in range(1,9):
                localsum =0 
                for j in range(2,8):
                    self.ConnectNodes(qp,xinit, yinit+i*yspace, xinit+xspace, yinit+j*yspace, matrix[i-1][j-2]) 
                    localsum += self.currentData[i-1]*float(matrix[i-1][j-2])
                mysum.append(localsum)
                self.drawNode(qp,xinit, yinit+i*yspace, 0, self.currentData[i-1])


            matrix = self.getWeights(2)
            xinit = xinit + xspace
            nextsum = []
            for i in range(2,8):
                localsum =0 
                for j in range(3,8):
                    self.ConnectNodes(qp,xinit, yinit+i*yspace, xinit+xspace, yinit+j*yspace-yspace/2, matrix[i-2][j-3]) 
                    localsum += mysum[i-2]*float(matrix[i-2][j-3])
                nextsum.append(localsum)
                self.drawNode(qp,xinit, yinit+i*yspace, 0, mysum[i-2])

            xinit = xinit + xspace
            for i in range(2,7):
                self.drawNode(qp,xinit, yinit+i*yspace + yspace/2, 1, nextsum[i-2])
        qp.end()

    def drawNode(self, qp, x, y, isend, colorlevel):
        if(colorlevel < -10):
            colorlevel = -10
        redLev = 1.0/(1.0+exp(-colorlevel))
        blueLev = 1.0/(1.0+exp(colorlevel))
        pen = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine)
        gradient = QtGui.QRadialGradient(x, y, 20, x,y)
        gradient.setColorAt(0, QtGui.QColor.fromRgbF(redLev, 0, blueLev, 1))
        if(isend == 1):
            gradient.setColorAt(0, QtGui.QColor.fromRgbF(blueLev, redLev, 0,1))


        gradient.setColorAt(1, QtGui.QColor.fromRgbF(0, 0, 0, 0.8))
        qp.setBrush(gradient)

        qp.setPen(pen)
        qp.drawEllipse(QtCore.QPointF(x,y),20,20);


    def ConnectNodes(self, qp, x1, y1, x2, y2, w):
        w = float(w)
        if(w < -10):
            w = 10
        pen = QtGui.QPen(QtCore.Qt.black, 8*1.0/(1.0+exp(-float(w))), QtCore.Qt.SolidLine)
        qp.setPen(pen)

        qp.drawLine(x1,y1,x2,y2)


def main():

    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
