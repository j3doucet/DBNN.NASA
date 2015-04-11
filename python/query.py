#functions for interacting with ipac and mpc
import wget
import re
import time
import math
import datetime
from os import walk

def get_ipac(ra_dec):
	url_query = "http://irsa.ipac.caltech.edu/cgi-bin/Gator/nph-query?catalog=wise_allwise_p3as_psd&spatial=cone&size=100&outfmt=1&selcols=w1mpro,w2mpro,w3mpro,w4mpro&&objstr="+ra_dec
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
			print "Interpolated: "+str(ra[0])+"h+"+str(ra[1])+"m+"+str(ra[2])+"s+"+str(dec[0])+"d"+str(dec[1])+"m"+str(dec[2])+"s"
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

def query_objects(mpec_data):
	tmp_out = open("tmp_out",'w')
	for entry in mpec_data:
		if entry['dec'][0]<0:
			dec_sign = "-"
		else:
			dec_sign = "+" 
		ra_dec = str(entry['ra'][0])+"h+"+str(entry['ra'][1])+"m+"+str(entry['ra'][2])+"s"+dec_sign+str(abs(entry['dec'][0]))+"d+"+str(entry['dec'][1])+"m+"+str(entry['dec'][2])+"s"
		tmp_out.write(ra_dec)
		print ra_dec
		#only do the first one until we're sure we got it right
		get_ipac(ra_dec)
		return
		
if __name__ == '__main__':
	mpec_data = parse_mpecs()
	#let's ignore interpolation for now...
	#interpolate_data(mpec_data)
	query_objects(mpec_data)