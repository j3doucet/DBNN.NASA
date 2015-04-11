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
		#self.dev_mode = True
		self.dev_mode = False
		QObject.connect(self.actionGetAsteroids, SIGNAL("triggered()"), self, SLOT("getAsteroids()"))
	#if we're developing, don't query the databases (reduce the load on web infrastructure)
	def getAsteroids(self):
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
if __name__ == '__main__':
	app = QApplication(sys.argv)
	frame = MainWindow()
	frame.show()
	sys.exit(app.exec_())
