from query import *
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
	def getAsteroids(self):
		self.StatusLabel.setText("Downloading MPECs")
		mpec_data = parse_mpecs()
		alternate_rows = False
		bg_color1 = "#DAC8B6"
		bg_color2 = "#E7DACE"
		font_size = "2pt"
		asteroid_text = "<table><tr bgcolor=\""+bg_color1+"\"><td><font face=\"verdana\" size=\""+font_size+"\"><b> Asteroid Name</td><td><font face=\"verdana\" size=\""+font_size+"\"><b>Ephemeris Date</td><td><font face=\"verdana\" size=\""+font_size+"\"><b>Coordinates</td><td><font face=\"verdana\" size=\""+font_size+"\"><b>Found WISE Source</td><td><font face=\"verdana\" size=\""+font_size+"\"><b>Light Curves</td></b></tr>"
		for mpec in mpec_data:
			ra_dec = formatCoords(mpec['ra'],mpec['dec'])
			if alternate_rows:
				bgcolor = bg_color1
				alternate_rows = False
			else:
				bgcolor= bg_color2
				alternate_rows = True
			asteroid_text+="<tr bgcolor=\""+bgcolor+"\"><td><font face=\"verdana\" size=\""+font_size+"\">"+mpec["name"]+"</td><td><font face=\"verdana\" size=\""+font_size+"\">"+mpec["closest_date"].strftime("%Y-%m-%d")+"</td><td><font face=\"verdana\" size=\""+font_size+"\">"+ra_dec+"</td><td><font face=\"verdana\" size=\""+font_size+"\">Not yet searched</td><td><font face=\"verdana\" size=\""+font_size+"\"></td></tr>"
		asteroid_text +="</font></table>"
		self.AsteroidBrowser.setHtml(asteroid_text)
		self.StatusLabel.setText("Searching WISE for matches")
if __name__ == '__main__':
	app = QApplication(sys.argv)
	frame = MainWindow()
	frame.show()
	sys.exit(app.exec_())
