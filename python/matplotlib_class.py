from matplotlib.figure import Figure
from matplotlib.pyplot import draw
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from PySide import QtGui
import math

class MatplotlibWidget(QtGui.QMainWindow):
	def __init__(self, parent=None):
		super(MatplotlibWidget, self).__init__()
		self.figure = Figure(facecolor='#000000',edgecolor='#000000')
		self.canvas = FigureCanvas(self.figure)
		self.axes = self.figure.add_subplot(111)
		self.xlabel = "Right Ascention (deg)"
		self.ylabel = "Declination (deg)"
		self.axes.set_xlabel(self.xlabel)
		self.axes.set_ylabel(self.ylabel)
		self.axes.set_axis_bgcolor('black')
		self.axes.spines['top'].set_color('white')
		self.axes.spines['bottom'].set_color('white')
		self.axes.spines['left'].set_color('white')
		self.axes.spines['right'].set_color('white')
		self.axes.xaxis.label.set_color('white')
		self.axes.yaxis.label.set_color('white')
		self.axes.tick_params(axis='x',colors='white')
		self.axes.tick_params(axis='y',colors='white')
		#print dir(self.axes)
		self.setGeometry(840, 500,760, 350)
		self.setWindowTitle('Map')
		self.setCentralWidget(self.canvas)
		self.show()
	def drawPlot(self,mpec_data):
		self.axes.clear()
		self.axes.set_xlabel(self.xlabel)
		self.axes.set_ylabel(self.ylabel)
		xvals_unclass = []
		xvals_class = []
		yvals_unclass = []
		yvals_class = []
		self.axes.set_ylim([-90,90])
		self.axes.set_xlim([0,360])
		for entry in mpec_data:
			ra = float(entry["ra"][0])*360/24+float(entry["ra"][1])+float(entry["ra"][2])*1/60.0
			dec = abs(float(entry["dec"][0]))+float(entry["dec"][1])/60.0+float(entry["dec"][2])*1/(60.0*60.0)
			math.copysign(dec,float(entry["dec"][0]))
			if "class" in entry.keys():
				xvals_class.append(ra)
				yvals_class.append(dec)
			else:
				xvals_unclass.append(ra)
				yvals_unclass.append(dec)
		self.axes.plot(xvals_unclass,yvals_unclass, 'wo')
		self.axes.plot(xvals_unclass,yvals_unclass, 'wo')
		self.axes.plot(xvals_class,yvals_class, 'ro')
		self.axes.plot(xvals_class,yvals_class, 'ro')
		self.canvas.draw()
		self.show()