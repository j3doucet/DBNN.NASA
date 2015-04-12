#format.py - contains functions related to data formatting
from query import *

def format_row(row_list,bg_color,fontface,fontsize,bold):
	output_str = "<tr bgcolor=\""+bg_color+"\">"
	for item in row_list:
		output_str += "<td><font face=\""+fontface+"\" size=\""+fontsize+"\">"
		if bold:
			output_str+="<b>"
		output_str +=item
		if bold:
			output_str+="</b>"
		output_str+="</font></td>"
	output_str+="</tr>"
	return output_str

#format the Right Ascention/ Declination coordinates into WISE format
def formatCoords(ra,dec):
	tmp_ra = [0,0,0]
	tmp_dec = [0,0,0]
	#if they are strings, switch them back to floats
	for i in range(0,3):
		tmp_ra[i] = float(ra[i])
		tmp_dec[i] = float(dec[i])
	if float(dec[0])<0:
		#print "negative dec!"
		dec_sign = "-"
	else:
		dec_sign = "+" 
	for i in range(0,2):
		tmp_ra[i] = "%02.f" % ra[i]
		tmp_dec[i] = "%02.f" % abs(dec[i])
	tmp_ra[2] = "%04.1f" %ra[2]
	tmp_dec[2] = "%02.f" %dec[2]
	ra_dec = tmp_ra[0]+"h+"+tmp_ra[1]+"m+"+tmp_ra[2]+"s"+dec_sign+tmp_dec[0]+"d+"+tmp_dec[1]+"m+"+tmp_dec[2]+"s"
	return ra_dec

def format_mpec_table(mpec_data):
	alternate_rows = False
	bg_color1 = "#DAC8B6"
	bg_color2 = "#E7DACE"
	font_face = "verdana"
	font_size = "2pt"
	asteroid_text= "<table>"
	asteroid_columns = ["Asteroid Name","Ephemeris Date","Coordinates","WISE Source","Light Curves","Class"]
	asteroid_text +=format_row(asteroid_columns,bg_color1,font_face,font_size,True)
	for mpec in mpec_data:
		#print mpec['ra']
		ra_dec = formatCoords(mpec['ra'],mpec['dec'])
		if alternate_rows:
			bgcolor = bg_color1
			alternate_rows = False
		else:
			bgcolor= bg_color2
			alternate_rows = True
		if "num_sources" in mpec.keys():
			if mpec["num_sources"]==0:
				search_status = "Not found!"
			if mpec["num_sources"]>0:
				search_status = str(mpec["num_sources"])+" found"
		else:
			search_status = "Not yet searched"
		light_curve = ""
		for k in range(1,5):
			key = "w"+str(k)+"mpro"
			if key in mpec.keys():
				light_curve+=mpec[key]
				if k!=4:
					light_curve+=","
		if "class" in mpec.keys():
			classification = mpec["class"]
		else:
			classification = ""
		asteroid_cells = [mpec["name"],mpec["closest_date"].strftime("%Y-%m-%d"),ra_dec,search_status,light_curve,classification]
		asteroid_text+=format_row(asteroid_cells,bgcolor,font_face,font_size,False)
	asteroid_text +="</table>"
	return asteroid_text