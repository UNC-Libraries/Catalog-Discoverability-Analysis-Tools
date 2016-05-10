# This script will download XML files using the TRLN Endeca web services API and then parse them for data 'match-points' to search for Syndetics matches.
# Results are written to a CSV file in the same directory script lives in
# Libby Wilcher (https://github.com/libbby/Syndetics-Catalog-Coverage-Assessment), UNC Chapel Hill
# Script written and tested in Python 2.7
# Script uses lxml library available at https://pypi.python.org/pypi/lxml/3.4.4
# Last updated: 9 May 2016

#		INSTRUCTIONS:
#	 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#	|																									|
#	|	1.) You will need the lxml library installed in your Python27\Lib directory. 					|
#	|		Find the appropriate copy for your machine here: https://pypi.python.org/pypi/lxml/3.4.4	|
#	|	2.) You will need a text file named BNums.txt in the same directory this script is stored.		|
#	|		Each line of the file must contain one (1) b-num of the format bXXXXXXX. Do not include 	|
#	|		opening or trailing spaces.																	|
#	|	3.) You will need a CSV named ____.csv in the same directory this script is stored. 			|
#	|		This CSV must be the output from the perl script ____.pl.									|
#	|	3.)	If, for whatever reason, you want each Endeca XML result opened in your web browser,		|
#	|		un-comment line __.																			|
#	|	4.) DO NOT remove the sleep time on line __. Bad things will probably happen, and your results	|
#	|		will be retrieved from Endeca progressively slower.											|
#	|	5.) This output from this script will be saved as a CSV file.									|
#	|																									|
#	 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

import webbrowser 
import lxml.etree as ET
import lxml.html as HTML
import urllib
import csv
import time

def isEbook(): # test for determing if item is an ebook
	global format_list
	format_list = []
	global ebook_format_boolean
	subtotal_ebook_format_boolean = 0
	f = 0
	fn = child.xpath('//Format/dimensionValues/item/name')
	for name in fn: #name in child.xpath('//Format/dimensionValues/item/name'):
		format_list.append(name.text)
		if format_list[f] == "eBook":
			ebook_format_boolean = 1
		else:
			ebook_format_boolean = 0
		subtotal_ebook_format_boolean += ebook_format_boolean
		f += 1
	if subtotal_ebook_format_boolean > 0:
		ebook_format_boolean = 1
	else:
		ebook_format_boolean = 0

def populateISBN():
	global isbn_list
	isbn_list = []
	ix = child.xpath('//fullRecordsList/item/properties/Syndetics-ISBN/item')
	for item in ix:
		isbn_list.append(item.text)
def isbn1SyndTest():
	global isbn1_summary_boolean
	global isbn1_toc_boolean
	global isbn1_dbc_boolean
	global isbn1_lc_boolean
	global isbn1_mc_boolean
	global isbn1_sc_boolean
	if len(isbn_list) > 0:
		syn_doch_isbn1 = HTML.parse(urllib.urlopen("http://syndetics.com/index.aspx?isbn=" + isbn_list[0] + "/XML.XML&client=ncchapelh")) # for missing Syndetics results, parse them as HTML
		if syn_doch_isbn1.find('head') != None: # passes a value of 0 to all booleans if the XML isn't even there (evident by way of present HTML tags, 'head' works fine.)
			isbn1_summary_boolean = 0
			isbn1_toc_boolean = 0
			isbn1_dbc_boolean = 0
			isbn1_lc_boolean = 0
			isbn1_mc_boolean = 0
			isbn1_sc_boolean = 0
		else:
			syn_docx_isbn1 = ET.parse(urllib.urlopen("http://syndetics.com/index.aspx?isbn=" + isbn_list[0] + "/XML.XML&client=ncchapelh")) # parse the Syndetics results as XML, because there were not HTML tags present.
			if syn_docx_isbn1.find('SUMMARY') != None: # Searches Syndetics XML for a 'SUMMARY' tag
				isbn1_summary_boolean = 1
			else:
				isbn1_summary_boolean = 0 
			if syn_docx_isbn1.find('TOC') != None: # Same as above, but for 'TOC' tag
				isbn1_toc_boolean = 1
			else:
				isbn1_toc_boolean = 0
			if syn_docx_isbn1.find('DBCHAPTER') != None: # Same as above, but for 'DBCHAPTER' tag
				isbn1_dbc_boolean = 1
			else:
				isbn1_dbc_boolean = 0
			if syn_docx_isbn1.find('LC') != None: # Same as above, but for 'LC' tag
				isbn1_lc_boolean = 1
			else:
				isbn1_lc_boolean = 0
			if syn_docx_isbn1.find('MC') != None: # Same as above, but for 'MC' tag
				isbn1_mc_boolean = 1
			else:
				isbn1_mc_boolean = 0
			if syn_docx_isbn1.find('SC') != None: # Same as above, but for 'SC' tag
				isbn1_sc_boolean = 1
			else:
				isbn1_sc_boolean = 0
	else:
		isbn1_summary_boolean = 0 # filter the CSV to differentiate items whose ISBN returns no Synetics info and items who do not HAVE ISBNs
		isbn1_toc_boolean = 0
		isbn1_dbc_boolean = 0
		isbn1_lc_boolean = 0
		isbn1_mc_boolean = 0
		isbn1_sc_boolean = 0

def oclcSynTest(): # use this function on each ITEM in the Endeca XML to search for Syndetics info using the OCLC number listed.
	global oclc_avsummary_boolean
	global oclc_toc_boolean
	global oclc_dbc_boolean
	global oclc_lc_boolean
	global oclc_mc_boolean
	global oclc_sc_boolean
	#if ebook_format_boolean == 0:
	if oclc_number == '':
		oclc_avsummary_boolean = 0
		oclc_toc_boolean = 0
		oclc_dbc_boolean = 0
		oclc_lc_boolean = 0
		oclc_mc_boolean = 0
		oclc_sc_boolean = 0
	else:
		syn_doch_oclc = HTML.parse(urllib.urlopen("http://syndetics.com/index.aspx?isbn=/XML.XML&client=ncchapelh&oclc=" + str(oclc_number))) # for missing Syndetics results, parse them as HTML
		if syn_doch_oclc.find('head') != None: # passes a value of 0 to all booleans if the XML isn't even there (evident by way of present HTML tags, 'head' works fine.)
			oclc_avsummary_boolean = 0
			oclc_toc_boolean = 0
			oclc_dbc_boolean = 0
			oclc_lc_boolean = 0
			oclc_mc_boolean = 0
			oclc_sc_boolean = 0
		else:
			syn_docx_oclc = ET.parse(urllib.urlopen("http://syndetics.com/index.aspx?isbn=/XML.XML&client=ncchapelh&oclc=" + str(oclc_number)))
			if syn_docx_oclc.find('AVSUMMARY') != None: # Searches Syndetics XML for a 'SUMMARY' tag
				oclc_avsummary_boolean = 1
			else:
				oclc_avsummary_boolean = 0 
			if syn_docx_oclc.find('TOC') != None: # Same as above, but for 'TOC' tag
				oclc_toc_boolean = 1
			else:
				oclc_toc_boolean = 0
			if syn_docx_oclc.find('DBCHAPTER') != None: # Same as above, but for 'DBCHAPTER' tag
				oclc_dbc_boolean = 1
			else:
				oclc_dbc_boolean = 0
			if syn_docx_oclc.find('LC') != None: # Same as above, but for 'LC' tag
				oclc_lc_boolean = 1
			else:
				oclc_lc_boolean = 0
			if syn_docx_oclc.find('MC') != None: # Same as above, but for 'MC' tag
				oclc_mc_boolean = 1
			else:
				oclc_mc_boolean = 0
			if syn_docx_oclc.find('SC') != None: # Same as above, but for 'SC' tag
				oclc_sc_boolean = 1
			else:
				oclc_sc_boolean = 0
			#urllib.urlretrieve("http://syndetics.com/index.aspx?isbn=/XML.XML&client=ncchapelh&oclc=" + oclc_number[0]
		
	#else:
	#	bool_oclc_summary = "null"
	#	oclc_toc_boolean = "null" 
	#	oclc_dbc_boolean = "null" 
	#	oclc_lc_boolean = "null"
	#	oclc_mc_boolean = "null"
	#	oclc_sc_boolean = "null"
	
def upcSynTest(): # use this function on each ITEM in the Endeca XML to search for Syndetics info using the OCLC number listed.
	global upc_avsummary_boolean
	global upc_toc_boolean
	global upc_dbc_boolean
	global upc_lc_boolean
	global upc_mc_boolean
	global upc_sc_boolean
	#if ebook_format_boolean == 0:
	if upc_number == None:
		upc_avsummary_boolean = 0
		upc_toc_boolean = 0
		upc_dbc_boolean = 0
		upc_lc_boolean = 0
		upc_mc_boolean = 0
		upc_sc_boolean = 0
	else:
		syn_doch_upc = HTML.parse(urllib.urlopen("http://syndetics.com/index.aspx?isbn=&upc=" + str(upc_number) + "/XML.XML&client=ncchapelh")) # for missing Syndetics results, parse them as HTML
		if syn_doch_upc.find('head') != None: # passes a value of 0 to all booleans if the XML isn't even there (evident by way of present HTML tags, 'head' works fine.)
			upc_avsummary_boolean = 0
			upc_toc_boolean = 0
			upc_dbc_boolean = 0
			upc_lc_boolean = 0
			upc_mc_boolean = 0
			upc_sc_boolean = 0
		else:
			syn_docx_upc = ET.parse(urllib.urlopen("http://syndetics.com/index.aspx?isbn=&upc=" + str(upc_number) + "/XML.XML&client=ncchapelh"))
			if syn_docx_upc.find('AVSUMMARY') != None: # Searches Syndetics XML for a 'SUMMARY' tag
				upc_avsummary_boolean = 1
			else:
				upc_avsummary_boolean = 0 
			if syn_docx_upc.find('TOC') != None: # Same as above, but for 'TOC' tag
				upc_toc_boolean = 1
			else:
				upc_toc_boolean = 0
			if syn_docx_upc.find('DBCHAPTER') != None: # Same as above, but for 'DBCHAPTER' tag
				upc_dbc_boolean = 1
			else:
				upc_dbc_boolean = 0
			if syn_docx_upc.find('LC') != None: # Same as above, but for 'LC' tag
				upc_lc_boolean = 1
			else:
				upc_lc_boolean = 0
			if syn_docx_upc.find('MC') != None: # Same as above, but for 'MC' tag
				upc_mc_boolean = 1
			else:
				upc_mc_boolean = 0
			if syn_docx_upc.find('SC') != None: # Same as above, but for 'SC' tag
				upc_sc_boolean = 1
			else:
				upc_sc_boolean = 0
			#urllib.urlretrieve("http://syndetics.com/index.aspx?isbn=&upc=" + upc_number[0] + "/XML.XML&client=ncchapelh")
		
	#else:
	#	upc_avsummary_boolean = "null"
	#	upc_toc_boolean = "null" 
	#	upc_dbc_boolean = "null" 
	#	upc_lc_boolean = "null"
	#	upc_mc_boolean = "null"
	#	upc_sc_boolean = "null"
	
def isbn2xSynTest():
	global isbn2x_summary_boolean
	global isbn2x_toc_boolean
	global isbn2x_dbc_boolean
	global isbn2x_lc_boolean
	global isbn2x_mc_boolean
	global isbn2x_sc_boolean
	global syn_docx_isbn2x
	total_isbn2x_summary_boolean = 0
	total_isbn2x_toc_boolean = 0
	total_isbn2x_dbc_boolean = 0
	total_isbn2x_lc_boolean = 0
	total_isbn2x_mc_boolean = 0
	total_isbn2x_sc_boolean = 0
	y = 0
	z = len(isbn_list)	# the number of ISBNs associated with the particular item
	if z > 1:	
		for y in range(z):	# loops through each ISBN
			if y > 0:	# y = 0 is our ISBN1, we already did that one
				syn_doch_isbn2x = HTML.parse(urllib.urlopen("http://syndetics.com/index.aspx?isbn=" + isbn_list[y] + "/XML.XML&client=ncchapelh"))	# for missing Syndetics results, parse them as HTML
				if syn_doch_isbn2x.find('head') != None:	# passes a value of 0 to all booleans if the XML isn't even there (evident by way of present HTML tags, 'head' works fine.)
					isbn2x_summary_boolean = 0
					isbn2x_toc_boolean = 0 
					isbn2x_dbc_boolean = 0
					isbn2x_lc_boolean = 0
					isbn2x_mc_boolean = 0
					isbn2x_sc_boolean = 0
				else:	# starting the booleans at 0, not because they WILL be empty, but because we will be summing.
					isbn2x_summary_boolean = 0
					isbn2x_toc_boolean = 0 
					isbn2x_dbc_boolean = 0
					isbn2x_lc_boolean = 0
					isbn2x_mc_boolean = 0
					isbn2x_sc_boolean = 0
					syn_docx_isbn2x = ET.parse(urllib.urlopen("http://syndetics.com/index.aspx?isbn=" + isbn_list[y] + "/XML.XML&client=ncchapelh"))
					if syn_docx_isbn2x.find('SUMMARY') != None: # Searches Syndetics XML for a 'SUMMARY' tag
						isbn2x_summary_boolean = 1
					else:
						isbn2x_summary_boolean = 0 
					if syn_docx_isbn2x.find('TOC') != None: # Same as above, but for 'TOC' tag
						isbn2x_toc_boolean = 1
					else:
						isbn2x_toc_boolean = 0
					if syn_docx_isbn2x.find('DBCHAPTER') != None: # Same as above, but for 'DBCHAPTER' tag
						isbn2x_dbc_boolean = 1
					else:
						isbn2x_dbc_boolean = 0
					if syn_docx_isbn2x.find('LC') != None: # Same as above, but for 'LC' tag
						isbn2x_lc_boolean = 1
					else:
						isbn2x_lc_boolean = 0
					if syn_docx_isbn2x.find('MC') != None: # Same as above, but for 'MC' tag
						isbn2x_mc_boolean = 1
					else:
						isbn2x_mc_boolean = 0
					if syn_docx_isbn2x.find('SC') != None: # Same as above, but for 'SC' tag
						isbn2x_sc_boolean = 1
					else:
						isbn2x_sc_boolean = 0
				total_isbn2x_summary_boolean += isbn2x_summary_boolean	# a running sum of whether any ISBN was associated with data type.
				total_isbn2x_toc_boolean += isbn2x_toc_boolean			# 0 means none were, 1 or more means at least one was.
				total_isbn2x_dbc_boolean += isbn2x_dbc_boolean
				total_isbn2x_lc_boolean += isbn2x_lc_boolean
				total_isbn2x_mc_boolean += isbn2x_mc_boolean
				total_isbn2x_sc_boolean += isbn2x_sc_boolean
			y += 1
			time.sleep(0.001)
		if total_isbn2x_summary_boolean > 0:	# turn those total_ variables into booleans for our CSV
			isbn2x_summary_boolean = 1
		if total_isbn2x_toc_boolean > 0:
			isbn2x_toc_boolean = 1
		if total_isbn2x_dbc_boolean > 0:
			isbn2x_dbc_boolean = 1
		if total_isbn2x_lc_boolean > 0:
			isbn2x_lc_boolean = 1
		if total_isbn2x_mc_boolean > 0:
			isbn2x_mc_boolean = 1
		if total_isbn2x_sc_boolean > 0:
			isbn2x_sc_boolean = 1
	else:	
		isbn2x_summary_boolean = 0
		isbn2x_toc_boolean = 0 
		isbn2x_dbc_boolean = 0
		isbn2x_lc_boolean = 0
		isbn2x_mc_boolean = 0
		isbn2x_sc_boolean = 0
			
def loopThroughInputList():
	global child
	
	endeca_url = "http://search.lib.unc.edu/search?R=UNC"+BNum+"&output-format=xml&record-options=include-record-facets"
	tree = ET.parse(endeca_url)	# set up XML tree to parse
	root = tree.getroot()
	for child in root:	# tells us (and script) what child is
		root.iter()
		
	parseXML()
			
def parseXML():
	global i
	global isbn_count
	global toc_boolean
	global main_author_boolean
	global other_author_count
	global primary_url_count
	global oclc_boolean
	global upc_boolean
	global oclc_number
	global upc_number
	i = 0
	
	isbn_count = int(child.xpath('count(//Syndetics-ISBN/item)'))
	other_author_count = int(child.xpath('count(//Other-Authors/item)'))
	primary_url_count = int(child.xpath('count(//Primary-URL/item)'))
	format_count = int(child.xpath('count(//Format/dimensionValues/item)'))
	isEbook()
	populateISBN()
		
	ice_toc = int(child.xpath('count(//ICE-Chapter-Title)'))
	if ice_toc > 0:
		toc_boolean = 1
	else:
		toc_boolean = 0
				
	main_author = int(child.xpath('count(//Main-Author)'))
	if main_author > 0:
		main_author_boolean = 1
	else:
		main_author_boolean = 0

	
	oclc = 0
	oclc = int(child.xpath('count(//fullRecordsList/item/properties/OCLCNumber)'))
	if oclc > 0:
		oclc_boolean = 1
		oclc_number = child.xpath('//fullRecordsList/item/properties/OCLCNumber/item/text()')
	else:
		oclc_boolean = 0
		oclc_number = 'NO OCLC'
				
	
	upc = 0
	upc = int(child.xpath('count(//fullRecordsList/item/properties/UPC)'))
	if upc > 0:
		upc_boolean = 1
		upc_number = child.xpath('//fullRecordsList/item/properties/UPC/item/text()')
	else:
		upc_boolean = 0
		upc_number = 'NO UPC'
		
	isbn1SyndTest()
	time.sleep(0.01)
	oclcSynTest()
	time.sleep(0.01)
	upcSynTest()
	time.sleep(0.01)
	isbn2xSynTest()
			
	#print(BNum, isbn_count, toc_boolean, main_author_boolean, other_author_count, primary_url_count, format_count, format_list, ebook_format_boolean, oclc_boolean, oclc_number, upc_boolean, upc_number, isbn_list)
	#print(BNum, isbn_count, isbn1_summary_boolean, isbn1_toc_boolean, isbn1_dbc_boolean, isbn1_lc_boolean, isbn1_mc_boolean, isbn1_sc_boolean)
	#print(BNum, oclc_avsummary_boolean, oclc_toc_boolean, oclc_dbc_boolean, oclc_lc_boolean, oclc_mc_boolean, oclc_sc_boolean)
	#print(BNum, upc_avsummary_boolean, upc_toc_boolean, upc_dbc_boolean, upc_lc_boolean, upc_mc_boolean, upc_sc_boolean)
	#print(BNum, isbn2x_summary_boolean, isbn2x_toc_boolean, isbn2x_dbc_boolean, isbn2x_lc_boolean, isbn2x_mc_boolean, isbn2x_sc_boolean)
	print(BNum, upc_boolean, upc_number, oclc_boolean, oclc_number)
	
	i += 1		
		
#with open('BNums.txt', 'r') as f:
with open('K-CSV.csv', 'r') as input_CSV:
	with open('L-CSV.csv', 'w') as output_CSV:#BNums = f.read().splitlines()
		reader = csv.reader(input_CSV)
		writer = csv.writer(output_CSV, lineterminator = '\n')
		
		all =[]
		row0 = reader.next()
		row0.append('ISBN COUNT')
		row0.append('TOC BOOLEAN')
		row0.append('MAIN AUTHOR BOOLEAN')
		row0.append('OTHER AUTHOR COUNT')
		row0.append('PRIMARY URL COUNT')
		row0.append('EBOOK FORMAT BOOLEAN')
		row0.append('OCLC BOOLEAN')
		row0.append('UPC BOOLEAN')
		row0.append('ISBN1: SUMMARY')
		row0.append('ISBN1: TOC')
		row0.append('ISBN1: DBC')
		row0.append('ISBN1: LC')
		row0.append('ISBN1: MC')
		row0.append('ISBN1: SC')
		row0.append('ISBN2X: SUMMARY')
		row0.append('ISBN2X: TOC')
		row0.append('ISBN2X: DBC')
		row0.append('ISBN2X: LC')
		row0.append('ISBN2X: MC')
		row0.append('ISBN2X: SC')
		row0.append('OCLC: AVSUMMARY')
		row0.append('OCLC: TOC')
		row0.append('OCLC: DBC')
		row0.append('OCLC: LC')
		row0.append('OCLC: MC')
		row0.append('OCLC: SC')
		row0.append('UPC: AVSUMMARY')
		row0.append('UPC: TOC')
		row0.append('UPC: DBC')
		row0.append('UPC: LC')
		row0.append('UPC: MC')
		row0.append('UPC: SC')
		all.append(row0)
		#print row0
				
		for row in reader:
			BNum = row[1]
			loopThroughInputList()
			row.append(isbn_count)
			row.append(toc_boolean)
			row.append(main_author_boolean)
			row.append(other_author_count)
			row.append(primary_url_count)
			row.append(ebook_format_boolean)
			row.append(oclc_boolean)
			row.append(upc_boolean)
			row.append(isbn1_summary_boolean)
			row.append(isbn1_toc_boolean)
			row.append(isbn1_dbc_boolean)
			row.append(isbn1_lc_boolean)
			row.append(isbn1_mc_boolean)
			row.append(isbn1_sc_boolean)
			row.append(isbn2x_summary_boolean)
			row.append(isbn2x_toc_boolean)
			row.append(isbn2x_dbc_boolean)
			row.append(isbn2x_lc_boolean)
			row.append(isbn2x_mc_boolean)
			row.append(isbn2x_sc_boolean)
			row.append(oclc_avsummary_boolean)
			row.append(oclc_toc_boolean)
			row.append(oclc_dbc_boolean)
			row.append(oclc_lc_boolean)
			row.append(oclc_mc_boolean)
			row.append(oclc_sc_boolean)
			row.append(upc_avsummary_boolean)
			row.append(upc_toc_boolean)
			row.append(upc_dbc_boolean)
			row.append(upc_lc_boolean)
			row.append(upc_mc_boolean)
			row.append(upc_sc_boolean)
			all.append(row)
			time.sleep(1.0)
		writer.writerows(all)
			
