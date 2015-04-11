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
	
def format_mpec_table(mpec_data):
	alternate_rows = False
	bg_color1 = "#DAC8B6"
	bg_color2 = "#E7DACE"
	font_face = "verdana"
	font_size = "2pt"
	asteroid_text= "<table>"
	asteroid_columns = ["Asteroid Name","Ephemeris Date","Coordinates","Found WISE Source","Light Curves"]
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
				search_status = "No sources found!"
			if mpec["num_sources"]==1:
				search_status = "1 source found" 
			if mpec["num_sources"]>1:
				search_status = str(mpec["num_sources"])+" sources found"
		else:
			search_status = "Not yet searched"
		if "w1mpro" in mpec.keys():
			light_curve = ""
			for i in range(1,5):
				key = "w"+str(i)+"mpro"
				light_curve+=mpec[key]
				if i!=4:
					light_curve+=","
		else:
			light_curve=""
		asteroid_cells = [mpec["name"],mpec["closest_date"].strftime("%Y-%m-%d"),ra_dec,search_status,light_curve]
		asteroid_text+=format_row(asteroid_cells,bgcolor,font_face,font_size,False)
	asteroid_text +="</table>"
	return asteroid_text