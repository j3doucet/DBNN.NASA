from query import *
from format import *
from DBNNMain import Ui_MainWindow
import PySide
from PySide.QtCore import *
from PySide.QtGui import *
import sys
from drawing import *


class MainWindow(QMainWindow, Ui_MainWindow):
	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)
		self.setupUi(self)
		self.setGeometry(0, 20,820, 900)
		#self.dev_mode = True
		self.dev_mode = False
		QObject.connect(self.actionGetAsteroids, SIGNAL("triggered()"), self, SLOT("getAsteroids()"))
		QObject.connect(self.actionLoad_Old_Data, SIGNAL("triggered()"), self, SLOT("loadOld()"))
		#self.NetworkObjects = QGraphicsScene()
		self.NetworkObjects = QPainter()
		self.NetworkView = Example()
		#self.drawNetwork()
	def loadOld(self):
		self.dev_mode = True
		self.run()
	def getAsteroids(self):
		self.dev_mode = False
		self.run()
	#if we're developing, don't query the databases (reduce the load on web infrastructure)
	def run(self):
		self.StatusLabel.setText("Downloading MPECs")
		if not self.dev_mode:
			get_mpecs(self)
		self.StatusLabel.setText("Parsing MPECs")
		mpec_data = parse_mpecs(self)
		self.AsteroidBrowser.setHtml(format_mpec_table(mpec_data))
		self.StatusLabel.setText("Searching WISE for matches")
		mpec_data= query_objects(mpec_data,self, not self.dev_mode)
		self.AsteroidBrowser.setHtml(format_mpec_table(mpec_data))
		self.StatusLabel.setText("Sending data to brain")
		mpec_data = generate_classifier(mpec_data,self)
		self.AsteroidBrowser.setHtml(format_mpec_table(mpec_data))
		self.StatusLabel.setText("Done!")
		self.ReadProgressBar.setValue(100)
	#draw the neural network
	def drawNetwork(self):
		#print dir(self.NetworkObjects)
		brush = QBrush(Qt.SolidPattern)
		self.NetworkObjects.setBrush(brush)
		self.NetworkObjects.drawEllipse(200,200,30,30)
		self.NetworkObjects.begin(self.NetworkView)
		#self.NetworkView.drawBrushes(self.NetworkObjects)
		self.NetworkObjects.begin()
if __name__ == '__main__':
	app = QApplication(sys.argv)
	frame = MainWindow()
	frame.show()
	sys.exit(app.exec_())
