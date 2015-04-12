from query import *
from format import *
from DBNNMain import Ui_MainWindow
import PySide
from PySide.QtCore import *
from PySide.QtGui import *
import sys
from drawing import *
from matplotlib_class import *

class MainWindow(QMainWindow, Ui_MainWindow):
	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)
		self.setupUi(self)
		self.setGeometry(0, 20,820, 900)
		#self.dev_mode = True
		self.dev_mode = False
		QObject.connect(self.actionGetAsteroids, SIGNAL("triggered()"), self, SLOT("getAsteroids()"))
		QObject.connect(self.actionLoad_Old_Data, SIGNAL("triggered()"), self, SLOT("loadOld()"))
		QObject.connect(self.actionQuit, SIGNAL("triggered()"), self, SLOT("closeAll()"))
		self.NetworkObjects = QPainter()
		self.NetworkView = Example()
		self.Map = MatplotlibWidget()
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
		print "dec 2 "+str(mpec_data[1]["dec"][0])
		mpec_tmp = mpec_data
		self.AsteroidBrowser.setHtml(format_mpec_table(mpec_tmp))
		self.StatusLabel.setText("Searching WISE for matches")
		mpec_data= query_objects(mpec_data,self, not self.dev_mode)
		self.Map.drawPlot(mpec_data)
		self.AsteroidBrowser.setHtml(format_mpec_table(mpec_data))
		self.StatusLabel.setText("Sending data to brain")
		mpec_data = generate_classifier(mpec_data,self)
		mpec_tmp = mpec_data
		self.AsteroidBrowser.setHtml(format_mpec_table(mpec_tmp))
		self.StatusLabel.setText("Done!")
		self.ReadProgressBar.setValue(100)
	def closeAll(self):
		self.Map.close()
		self.NetworkView.close()
		self.close()
if __name__ == '__main__':
	app = QApplication(sys.argv)
	frame = MainWindow()
	frame.show()
	sys.exit(app.exec_())
