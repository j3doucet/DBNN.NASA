#functions for interacting with ipac and mpc
import wget
import re
import time
import os
import math
import datetime
from format import *
from os import walk
from PySide.QtCore import QCoreApplication

#if new_query is set to false, we will instead look at the last file, not query irsa again.
def get_ipac(ra_dec,new_query=True):
	if new_query:
		#remove any stale queries
		if os.path.exists("nph-query"):
			os.remove("nph-query")
		#if we don't find anything within a cone of 100 arcseconds from our coordinates, we probably don't have a good image
		radius = 100
		url_query = "http://irsa.ipac.caltech.edu/cgi-bin/Gator/nph-query?outfmt=1&objstr="+ra_dec+"&spatial=Cone&radius="+str(radius)+"&catalog=wise_allwise_p3as_psd"
		result = wget.download(url_query)
	else:
		result = "nph-query"
	#assuming we found multiple sources, we need to figure out which one is closest to our actual search
	f = open(result,"r")
	filled_keys = False
	num_sources = 0
	sources = []
	for line in f:
		result = line.find("SKYAREA")
		if result>0:
			parts = line.split("=")
			ra = float(parts[2].replace("dec",""))
			dec = float(parts[3].split()[0])
		#get the guide to the columns
		if line[0] =='|' and not filled_keys:
			keys = line.split("|")
			filled_keys = True
		if line[0] !='|' and line[0] !='\\':
			row = {}
			columns = line.split()
			for i in range(0,len(columns)):
				keys[i+1] = keys[i+1].strip()
				row[keys[i+1]] = columns[i]
			num_sources+=1
			sources.append(row)
	#assuming that multiple sources were found, pick out the closest one
	num_sources = len(sources)
	closest_distance = 1000000000
	for entry in sources:
		distance = math.sqrt((float(entry["ra"])-ra)**2+(float(entry["dec"])-dec)**2)
		if distance<closest_distance:
			closest_distance = distance
			closest_entry = entry
	return [num_sources,closest_entry]

def mpc_query():
	mpc_query = "http://www.minorplanetcenter.net/db_search/show_by_date?utf8=%E2%9C%93&start_date=2015-04-08&end_date=2015-04-09&observatory_code=+--+All+--+&obj_type=all"
	mpc_query = wget.download(url_query)
	f = open(mpc_query,"r")

def get_mpecs(mainWindow,new_file = False):
	if new_file:
		#delete the stale data
		if os.path.exists("RecentMPECs.html"):
			os.remove("RecentMPECs.html")
		mpec_filename = wget.download("http://www.minorplanetcenter.net/mpec/RecentMPECs.html")
	else:
		mpec_filename = "RecentMPECs.html"
	f = open(mpec_filename,"r")
	prev_line = False
	start_reading = False
	lines = f.readlines()
	for i in range(0,len(lines)):
		#mpc changed their data format overnight...
		if lines[i] =='<!-- Main content block -->\n':
			start_reading = True
		'''
		if lines[i] == '<ul>\n' and prev_line:
			start_reading = True 
		if lines[i] =='</p><p></p><hr>\n':
			prev_line = True
		else:
			prev_line = False
		'''
		if start_reading:
			result = re.match("<p><li>",lines[i])
			if result:
				columns = lines[i].split('"')
				#check to see if we already have the file, if not, download it.
				html_filename = columns[1].split("/")[-1]
				if not os.path.exists(html_filename):
					#deal with local links
					if not re.match("http",columns[1]):
						columns[1] = "http://www.minorplanetcenter.net"+columns[1]
					print "downloading: "+columns[1]
					result = wget.download(columns[1])
					time.sleep(1)
		mainWindow.ReadProgressBar.setValue(25*i/len(lines))

def parse_mpecs(mainWindow):
	mpec_data = []
	today = datetime.date.today()
	mainWindow.ReadProgressBar.setValue(25)
	good_filenames = []
	for (dirpath, dirnames, filenames) in walk("."):
		for file in filenames:
			if file.endswith(".html") and file != "RecentMPECs.html":
				good_filenames.append(file)
	for i in range(0,len(good_filenames)):
		mainWindow.ReadProgressBar.setValue(25+25*i/len(good_filenames))
		line_number = 0
		f = open(good_filenames[i],"r")
		start_reading = False
		first_line = False
		closest_date = datetime.date(1990,1,1)
		next_closest_date = datetime.date(1990,1,1)
		ra = ""
		asteroid_name = ""
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
	return mpec_data
#some of the ephemeris don't line up with the current date, if so, interpolate between the last couple of days 
def interpolate_data(mpec_data):
	today = datetime.date.today()
	interpolated_mpec = []
	for entry in mpec_data:
		if entry["closest_date"] == today:
			ra = entry['ra']
			dec = entry['dec']
			print "ephemeris found for today, horay!"
		else:
			#we need to linearly extrapolate the distance between the two dates to today's date
			ra = subtract_times(entry['ra'],entry['last_ra'])
			dec = subtract_times(entry['dec'],entry['last_dec'])
			for i in range(0,3):
				ra[i] = ra[i]*float(today)/float(entry['closest_date']-entry['next_date'])+entry['ra'][i]
				dec[i] = dec[i]*float(today)/float(entry['closest_date']-entry['next_date'])+entry['dec'][i]
			ra_dec = formatCoords(ra,dec)
			print "Interpolated: "+ra_dec

#returns ra1-ra2
def subtract_times(ra1,ra2):
	ra = [0,0,0]
	#if we're dealing with declinations, we need to make sure that the two are in the same direction
	if math.copysign(1,ra1[0]) != math.copysign(1,ra2[0]):
		if math.copysign(1,ra1[0])==1:
			ra[0] = ra1[0]+abs(ra2[0])
		else:
			ra[0] = -(ra1[0]+abs(ra2[0]))
		ra[1] = ra1[1]+ra2[1]
		ra[2] = ra1[2]+ra2[2]
	else:
		ra[0] = ra1[0]-ra2[0]
		ra[1] = ra1[1]-ra2[1]
		ra[2] = ra1[2]-ra2[2]
		#now to correct the values
		#seconds
		if ra[2]<0.0:
			ra[2] += 60.0
			ra[1] -= 1
		if ra[2]>=60.0:
			ra[2] = ra[2]-60.0
			ra[1]+=1
		#minutes
		if ra[1]<0.0:
			ra[1] += 60.0
			if math.copysign(1,ra1[0])==-1:
				ra[0] += 1
			else:
				ra[0] -= 1
		if ra[1]>=60.0:
			ra[1] = ra[1]-60.0
			if math.copysign(1,ra1[0])==-1:
				ra[0]-=1
			else:
				ra[0]+=1
	return ra

#for each entry in the mpec data, search for the object in WISE and extract the W's of the closest source
def query_objects(mpec_data,mainWindow,new_query = True):
	wise_filename = "WISE_results.csv"
	if new_query:
		mpec_data_new = []
		for i in range(0,len(mpec_data)):
			print "Querying "+str(i)+" out of "+str(len(mpec_data))
			mainWindow.ReadProgressBar.setValue(50+25*i/len(mpec_data))
			QCoreApplication.processEvents()
			entry = mpec_data[i]
			ra_dec = formatCoords(entry['ra'],entry['dec'])
			#only do the first one until we're sure we got it right
			[num_sources, closest_entry] = get_ipac(ra_dec,new_query)
			mpec_data[i]["num_sources"] = num_sources
			for j in range(1,5):
				key = "w"+str(j)+"mpro"
				mpec_data[i][key] = closest_entry[key]
			mainWindow.AsteroidBrowser.setHtml(format_mpec_table(mpec_data))
			QCoreApplication.processEvents()
		#write this data to a file for future use
		f_out = open(wise_filename,"w+")
		keys = mpec_data[0].keys()
		f_out.write(",".join(keys)+"\n")
		for entry in mpec_data:
			f_out.write(",".join(entry)+"\n")
		f_out.close()
	else:
		#load old data
		if not os.path.exists(wise_filename):
			print "File not found!"
			return 0
		f_in = open(wise_filename,"r")
		lines = f_in.readlines()
		mpec_data = []
		for i in range(0,len(lines)):
			if i ==0:
				keys = lines.split(",")
			else:
				row = []
				cells = lines.split(",")
				for j in range(0,len(cells)):
					row[keys[j]]=cells[j]
				mpec_data.append(row)
	return mpec_data

if __name__ == '__main__':
	mpec_data = parse_mpecs()
	#let's ignore interpolation for now...
	#interpolate_data(mpec_data)
	query_objects(mpec_data,False)