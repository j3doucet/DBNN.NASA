from query import *
from format import *
from DBNNMain import Ui_MainWindow
import PySide
from PySide.QtCore import *
from PySide.QtGui import *
import sys


class MainWindow(QMainWindow, Ui_MainWindow):
	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)
		self.setupUi(self)
		QObject.connect(self.actionGetAsteroids, SIGNAL("triggered()"), self, SLOT("getAsteroids()"))
	#if we're developing, don't query the databases (reduce the load on web infrastructure)
	def getAsteroids(self,dev_mode = True):
		self.StatusLabel.setText("Downloading MPECs")
		mpec_data = parse_mpecs()
		self.AsteroidBrowser.setHtml(format_mpec_table(mpec_data))
		self.StatusLabel.setText("Searching WISE for matches")
		mpec_data= query_objects(mpec_data, not dev_mode)
		self.AsteroidBrowser.setHtml(format_mpec_table(mpec_data))
if __name__ == '__main__':
	app = QApplication(sys.argv)
	frame = MainWindow()
	frame.show()
	sys.exit(app.exec_())
