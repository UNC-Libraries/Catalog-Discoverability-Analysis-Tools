# This script will download XML files using the TRLN Endeca web services API and then parse them for data 'match-points' to search for Syndetics Solutions matches.
# Results are written to a CSV file in the same directory that the script lives in. 
# Written by Libby Wilcher at UNC Chapel Hill
# Script written and tested in Python 2.7
# Script uses lxml library available at https://pypi.python.org/pypi/lxml/3.4.4
# Last updated: 14 March 2017

#	INSTRUCTIONS:
#	1.) You will need the lxml library installed in your Python27\Lib directory. Find the appropriate copy for your machine here: https://pypi.python.org/pypi/lxml/3.4.4
#	2.) You will need a CSV named input.csv in the same directory this script is stored. This CSV must be the output from the perl script ecoll_catalog_eval_2.pl.
#	3.) If, for whatever reason, you want each Endeca XML result opened in your web browser, un-comment lines beginning with "webbrowser.open(".
#	4.) DO NOT remove the sleep time when making calls to the Endeca server. Bad things will probably happen, and your results will be retrieved from Endeca progressively slower.
#	5.) This output from this script will be saved as a CSV file called output_file.csv.

import webbrowser 
import lxml.etree as ET
import lxml.html as HTML
import urllib
import csv
import time
import logging

logger = logging.getLogger('errors')
hdlr = logging.FileHandler('errors.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.DEBUG)

def testForEbookFormat(): # test for determing if item is an ebook
	global format_list
	format_list = [] # will be an array containing every string in the Endeca XML's format tag
	global ebook_format_boolean # 1= at least one of the format strings provided in the XML is "eBook". 0= None of listed formats are "eBook."
	subtotal_ebook_format_boolean = 0 
	f = 0 # position in the list
	fx = child.xpath('//Format/dimensionValues/item/name')
	for name in fx: #name in child.xpath('//Format/dimensionValues/item/name'):
		format_list.append(name.text) #appends the string from Endeca XML tag to format_list
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

def populateISBN(): #grab all Syndetics ISBNs from the Endeca XML and put into an array
	global isbn_list
	isbn_list = []
	ix = child.xpath('//fullRecordsList/item/properties/Syndetics-ISBN/item')
	for item in ix:#cycle through each item tag in Syndetics-ISBN
		isbn_list.append(item.text)

def isbn1SynTest(): #round of tests using the FIRST Syndetics ISBN listed in the XML. We are querying Syndetics, using only that ISBN, to check for the presence of summary/toc/dbc/lc/mc/sc
	global isbn1_summary_boolean
	global isbn1_toc_boolean
	global isbn1_dbc_boolean
	global isbn1_lc_boolean
	global isbn1_mc_boolean
	global isbn1_sc_boolean
	if isbn_count > 0: #if there exist any syndetics ISBNs listed in the Endeca XML
		#webbrowser.open("http://syndetics.com/index.aspx?isbn=" + isbn_list[0] + "/XML.XML&client=ncchapelh")
		syn_doch_isbn1 = HTML.parse(urllib.urlopen("http://syndetics.com/index.aspx?isbn=" + isbn_list[0] + "/XML.XML&client=ncchapelh")) # for missing Syndetics results, parse them as HTML
		if syn_doch_isbn1.find('head') is not None: # passes a value of 0 to all booleans if the XML isn't even there (evident by way of present HTML tags, 'head' works fine.)
			isbn1_summary_boolean = 0
			isbn1_toc_boolean = 0
			isbn1_dbc_boolean = 0
			isbn1_lc_boolean = 0
			isbn1_mc_boolean = 0
			isbn1_sc_boolean = 0
		else:# parse the Syndetics results as XML, because there were not HTML tags present.
			syn_docx_isbn1 = ET.parse(urllib.urlopen("http://syndetics.com/index.aspx?isbn=" + isbn_list[0] + "/XML.XML&client=ncchapelh")) 
			if syn_docx_isbn1.find('SUMMARY') is not None: # Searches Syndetics XML for a 'SUMMARY' tag
				isbn1_summary_boolean = 1
			else:
				isbn1_summary_boolean = 0 
			if syn_docx_isbn1.find('TOC') is not None: # Same as above, but for 'TOC' tag
				isbn1_toc_boolean = 1
			else:
				isbn1_toc_boolean = 0
			if syn_docx_isbn1.find('DBCHAPTER') is not None: # Same as above, but for 'DBCHAPTER' tag
				isbn1_dbc_boolean = 1
			else:
				isbn1_dbc_boolean = 0
			if syn_docx_isbn1.find('LC') is not None: # Same as above, but for 'LC' tag
				isbn1_lc_boolean = 1
			else:
				isbn1_lc_boolean = 0
			if syn_docx_isbn1.find('MC') is not None: # Same as above, but for 'MC' tag
				isbn1_mc_boolean = 1
			else:
				isbn1_mc_boolean = 0
			if syn_docx_isbn1.find('SC') is not None: # Same as above, but for 'SC' tag
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

def oclcSynTest(): #round of tests to search for Syndetics info using the OCLC number listed in the Endeca XML.
	global oclc_summary_boolean
	global oclc_toc_boolean
	global oclc_dbc_boolean
	global oclc_lc_boolean
	global oclc_mc_boolean
	global oclc_sc_boolean
	if oclc_boolean == 1: #if there is an OCLC number listed in the Endeca XML
		#webbrowser.open("http://syndetics.com/index.aspx?isbn=/XML.XML&client=ncchapelh&oclc=" + str(oclc_number[0]))
		syn_doch_oclc = HTML.parse(urllib.urlopen("http://syndetics.com/index.aspx?isbn=/XML.XML&client=ncchapelh&oclc=" + str(oclc_number[0]))) # for missing Syndetics results, parse them as HTML
		if syn_doch_oclc.find('head') is not None: # passes a value of 0 to all booleans if the XML isn't even there (evident by way of present HTML tags, 'head' works fine.)
			oclc_summary_boolean = 0
			oclc_toc_boolean = 0
			oclc_dbc_boolean = 0
			oclc_lc_boolean = 0
			oclc_mc_boolean = 0
			oclc_sc_boolean = 0
		else:# parse the Syndetics results as XML, because there were not HTML tags present.
			syn_docx_oclc = ET.parse(urllib.urlopen("http://syndetics.com/index.aspx?isbn=/XML.XML&client=ncchapelh&oclc=" + str(oclc_number[0])))
			if syn_docx_oclc.find('SUMMARY') is not None: # Searches Syndetics XML for an 'AVSUMMARY' tag
				oclc_summary_boolean = 1
			else:
				oclc_summary_boolean = 0 
			if syn_docx_oclc.find('TOC') is not None: # Same as above, but for 'TOC' tag
				oclc_toc_boolean = 1
			else:
				oclc_toc_boolean = 0
			if syn_docx_oclc.find('DBCHAPTER') is not None: # Same as above, but for 'DBCHAPTER' tag
				oclc_dbc_boolean = 1
			else:
				oclc_dbc_boolean = 0
			if syn_docx_oclc.find('LC') is not None: # Same as above, but for 'LC' tag
				oclc_lc_boolean = 1
			else:
				oclc_lc_boolean = 0
			if syn_docx_oclc.find('MC') is not None: # Same as above, but for 'MC' tag
				oclc_mc_boolean = 1
			else:
				oclc_mc_boolean = 0
			if syn_docx_oclc.find('SC') is not None: # Same as above, but for 'SC' tag
				oclc_sc_boolean = 1
			else:
				oclc_sc_boolean = 0
	else: #if there is no OCLC number listed in the Endeca XML
		oclc_summary_boolean = 0
		oclc_toc_boolean = 0
		oclc_dbc_boolean = 0
		oclc_lc_boolean = 0
		oclc_mc_boolean = 0
		oclc_sc_boolean = 0		
def upcSynTest(): #round of tests to search for Syndetics info using the UPC listed in the Endeca XML.
	global upc_avsummary_boolean
	global upc_toc_boolean
	global upc_dbc_boolean
	global upc_lc_boolean
	global upc_mc_boolean
	global upc_sc_boolean
	#if ebook_format_boolean == 0:
	if upc_boolean == 1: #if there is a UPC listed in the Endeca XML
		#webbrowser.open("http://syndetics.com/index.aspx?isbn=&upc=" + str(upc_number[0]) + "/XML.XML&client=ncchapelh")
		syn_doch_upc = HTML.parse(urllib.urlopen("http://syndetics.com/index.aspx?isbn=&upc=" + str(upc_number[0]) + "/XML.XML&client=ncchapelh")) # for missing Syndetics results, parse them as HTML
		if syn_doch_upc.find('head') is not None: # passes a value of 0 to all booleans if the XML isn't even there (evident by way of present HTML tags, 'head' works fine.)
			upc_avsummary_boolean = 0
			upc_toc_boolean = 0
			upc_dbc_boolean = 0
			upc_lc_boolean = 0
			upc_mc_boolean = 0
			upc_sc_boolean = 0
		else:# parse the Syndetics results as XML, because there were not HTML tags present.
			syn_docx_upc = ET.parse(urllib.urlopen("http://syndetics.com/index.aspx?isbn=&upc=" + str(upc_number[0]) + "/XML.XML&client=ncchapelh"))
			if syn_docx_upc.find('AVSUMMARY') is not None: # Searches Syndetics XML for an 'AVSUMMARY' tag
				upc_avsummary_boolean = 1
			else:
				upc_avsummary_boolean = 0 
			if syn_docx_upc.find('TOC') is not None: # Same as above, but for 'TOC' tag
				upc_toc_boolean = 1
			else:
				upc_toc_boolean = 0
			if syn_docx_upc.find('DBCHAPTER') is not None: # Same as above, but for 'DBCHAPTER' tag
				upc_dbc_boolean = 1
			else:
				upc_dbc_boolean = 0
			if syn_docx_upc.find('LC') is not None: # Same as above, but for 'LC' tag
				upc_lc_boolean = 1
			else:
				upc_lc_boolean = 0
			if syn_docx_upc.find('MC') is not None: # Same as above, but for 'MC' tag
				upc_mc_boolean = 1
			else:
				upc_mc_boolean = 0
			if syn_docx_upc.find('SC') is not None: # Same as above, but for 'SC' tag
				upc_sc_boolean = 1
			else:
				upc_sc_boolean = 0
	else:#if there is no UPC listed in the Endeca XML
		upc_avsummary_boolean = 0
		upc_toc_boolean = 0
		upc_dbc_boolean = 0
		upc_lc_boolean = 0
		upc_mc_boolean = 0
		upc_sc_boolean = 0
	
def isbn2xSynTest():#round of tests using the second and all subsequent Syndetics ISBNs from and item's Endeca XML
	global isbn2x_summary_boolean
	global isbn2x_toc_boolean
	global isbn2x_dbc_boolean
	global isbn2x_lc_boolean
	global isbn2x_mc_boolean
	global isbn2x_sc_boolean
	global syn_docx_isbn2x
	subtotal_isbn2x_summary_boolean = 0
	subtotal_isbn2x_toc_boolean = 0
	subtotal_isbn2x_dbc_boolean = 0
	subtotal_isbn2x_lc_boolean = 0
	subtotal_isbn2x_mc_boolean = 0
	subtotal_isbn2x_sc_boolean = 0
	y = 0
	z = len(isbn_list)	# the number of ISBNs associated with the particular item
	if z > 1:	
		for y in range(z):	# loops through each ISBN
			if y > 0:	# y = 0 is our ISBN1, we already did that one
				#webbrowser.open("http://syndetics.com/index.aspx?isbn=" + isbn_list[y] + "/XML.XML&client=ncchapelh")
				syn_doch_isbn2x = HTML.parse(urllib.urlopen("http://syndetics.com/index.aspx?isbn=" + isbn_list[y] + "/XML.XML&client=ncchapelh"))	# for missing Syndetics results, parse them as HTML
				if syn_doch_isbn2x.find('head') is not None:	# passes a value of 0 to all booleans if the XML isn't even there (evident by way of present HTML tags, 'head' works fine.)
					isbn2x_summary_boolean = 0
					isbn2x_toc_boolean = 0 
					isbn2x_dbc_boolean = 0
					isbn2x_lc_boolean = 0
					isbn2x_mc_boolean = 0
					isbn2x_sc_boolean = 0
				else:	# parse the Syndetics results as XML, because there were not HTML tags present. 
					isbn2x_summary_boolean = 0 #starting the booleans at 0, not because they WILL be empty, but because we will be summing.
					isbn2x_toc_boolean = 0 
					isbn2x_dbc_boolean = 0
					isbn2x_lc_boolean = 0
					isbn2x_mc_boolean = 0
					isbn2x_sc_boolean = 0
					syn_docx_isbn2x = ET.parse(urllib.urlopen("http://syndetics.com/index.aspx?isbn=" + isbn_list[y] + "/XML.XML&client=ncchapelh"))
					if syn_docx_isbn2x.find('SUMMARY') is not None: # Searches Syndetics XML for a 'SUMMARY' tag
						isbn2x_summary_boolean = 1
					else:
						isbn2x_summary_boolean = 0 
					if syn_docx_isbn2x.find('TOC') is not None: # Same as above, but for 'TOC' tag
						isbn2x_toc_boolean = 1
					else:
						isbn2x_toc_boolean = 0
					if syn_docx_isbn2x.find('DBCHAPTER') is not None: # Same as above, but for 'DBCHAPTER' tag
						isbn2x_dbc_boolean = 1
					else:
						isbn2x_dbc_boolean = 0
					if syn_docx_isbn2x.find('LC') is not None: # Same as above, but for 'LC' tag
						isbn2x_lc_boolean = 1
					else:
						isbn2x_lc_boolean = 0
					if syn_docx_isbn2x.find('MC') is not None: # Same as above, but for 'MC' tag
						isbn2x_mc_boolean = 1
					else:
						isbn2x_mc_boolean = 0
					if syn_docx_isbn2x.find('SC') is not None: # Same as above, but for 'SC' tag
						isbn2x_sc_boolean = 1
					else:
						isbn2x_sc_boolean = 0
				subtotal_isbn2x_summary_boolean += isbn2x_summary_boolean	# a running sum of whether any ISBN was associated with data type.
				subtotal_isbn2x_toc_boolean += isbn2x_toc_boolean			# 0 means none were, 1 or more means at least one was.
				subtotal_isbn2x_dbc_boolean += isbn2x_dbc_boolean
				subtotal_isbn2x_lc_boolean += isbn2x_lc_boolean
				subtotal_isbn2x_mc_boolean += isbn2x_mc_boolean
				subtotal_isbn2x_sc_boolean += isbn2x_sc_boolean
			y += 1
			time.sleep(0.001)
		if subtotal_isbn2x_summary_boolean > 0:	# turn those subtotal_ variables into booleans for our CSV
			isbn2x_summary_boolean = 1
		if subtotal_isbn2x_toc_boolean > 0:
			isbn2x_toc_boolean = 1
		if subtotal_isbn2x_dbc_boolean > 0:
			isbn2x_dbc_boolean = 1
		if subtotal_isbn2x_lc_boolean > 0:
			isbn2x_lc_boolean = 1
		if subtotal_isbn2x_mc_boolean > 0:
			isbn2x_mc_boolean = 1
		if subtotal_isbn2x_sc_boolean > 0:
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
	#webbrowser.open(endeca_url)
	
	while True:
		try:
			tree = ET.parse(endeca_url)	# set up XML tree to parse
			root = tree.getroot()
			for child in root:	# tells us (and script) what child is
				root.iter()
			parseXML()
			break
		except ET.XMLSyntaxError:
			logger.exception(BNum)
			print(BNum)
			
def parseXML():#parses the Endeca XML
	global i
	global isbn_count
	global ice_ct_boolean
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
	testForEbookFormat()
	populateISBN()
		
	ice_ct = int(child.xpath('count(//ICE-Chapter-Title)'))
	if ice_ct > 0:
		ice_ct_boolean = 1
	else:
		ice_ct_boolean = 0
				
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
		
	isbn1SynTest()
	time.sleep(0.01)
	oclcSynTest()
	time.sleep(0.01)
	upcSynTest()
	time.sleep(0.01)
	isbn2xSynTest()
	
	i += 1		

with open('input_file.csv', 'r') as input_CSV:
	with open('output_file.csv', 'w') as output_CSV:
		reader = csv.reader(input_CSV)
		writer = csv.writer(output_CSV, lineterminator = '\n')
		
		all =[]
		row0 = reader.next()
		row0.append('ISBN COUNT')
		row0.append('ICE-CT BOOLEAN')
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
		row0.append('OCLC: SUMMARY')
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
			row.append(ice_ct_boolean)
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
			row.append(oclc_summary_boolean)
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
