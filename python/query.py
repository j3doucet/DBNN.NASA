#functions for interacting with ipac and mpc
import wget
import re
import time
import datetime
from os import walk

def get_ipac(ra_dec):
	url_query = "http://irsa.ipac.caltech.edu/cgi-bin/Gator/nph-query?catalog=wise_allwise_p3as_psd&spatial=cone&size=100&outfmt=1&selcols=w1mpro,w2mpro,w3mpro,w4mpro&&objstr=00h+42m+44.32s+41d+16m+08.5s"
	result = wget.download(url_query)
	result = "nph-query"
	f = open(result,"r")
	for line in f:
		if line[0] !='|' and line[0] !='\\':
			columns = line.split()
			print columns

def mpc_query():
	mpc_query = "http://www.minorplanetcenter.net/db_search/show_by_date?utf8=%E2%9C%93&start_date=2015-04-08&end_date=2015-04-09&observatory_code=+--+All+--+&obj_type=all"
	mpc_query = wget.download(url_query)
	f = open(mpc_query,"r")

def get_mpecs():
	mpec_filename = wget.download("http://www.minorplanetcenter.net/mpec/RecentMPECs.html")
	f = open(mpec_filename,"r")
	prev_line = False
	start_reading = False
	for line in f:
		if line == '<ul>\n' and prev_line:
			start_reading = True 
		if line =='</p><p></p><hr>\n':
			prev_line = True
		else:
			prev_line = False
		if start_reading:
			result = re.match("<p></p>",line)
			if result:
				columns = line.split('"')
				result = wget.download(columns[1])

def parse_mpecs():
	mpec_data = []
	today = datetime.date.today()
	for (dirpath, dirnames, filenames) in walk("."):
		for file in filenames:
			if file.endswith(".html"):
				line_number = 0
				f = open(file,"r")
				start_reading = False
				first_line = False
				closest_date = datetime.date(1990,1,1)
				next_closest_date = datetime.date(1990,1,1)
				asteroid_name = ""
				ra = ""
				dec = ""
				for line in f:
					line_number+=1
					if start_reading:
						columns = line.split()
						if first_line:
							asteroid_name = columns[1] 
							first_line = False
						if len(columns) ==14:
							date = datetime.date(int(columns[0]),int(columns[1]),int(columns[2]))
							if abs(date-today)<abs(closest_date-date):
								next_closest_date = closest_date
								last_ra = ra
								last_dec = dec
								closest_date = date
								ra = [float(columns[3]),float(columns[4]),float(columns[5])]
								dec = [float(columns[6]),float(columns[7]),float(columns[8])]
						if re.match("<b>",line):
							start_reading = False
					if line =="Ephemeris:\n":
						start_reading = True
						first_line = True
				if closest_date != datetime.date(1990,1,1):
					row = {"name":asteroid_name,"closest_date":closest_date,"next_date":next_closest_date,"ra":ra,"dec":dec,"last_ra":last_ra,"last_dec":last_dec}
					mpec_data.append(row)

parse_mpecs()