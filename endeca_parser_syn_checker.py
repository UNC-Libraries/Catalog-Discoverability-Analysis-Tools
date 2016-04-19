# This script will download XML files using the TRLN Endeca web services API and then parse them for data 'match-points' to search for Syndetics matches.
# Results are written to a CSV file in the same directory script lives in
# Libby Wilcher (https://github.com/libbby/Syndetics-Catalog-Coverage-Assessment), UNC Chapel Hill
# Script written and tested in Python 2.7
# Script uses lxml library available at https://pypi.python.org/pypi/lxml/3.4.4
# Last updated: 19 April 2016

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
	global is_ebook
	global is_ebook
	is_ebook = []
	global bool_is_ebook
	total_bool_is_ebook = 0
	f = 0
	#while f < format_count:
	fn = child.xpath('//Format/dimensionValues/item/name')
	for name in fn:#name in child.xpath('//Format/dimensionValues/item/name'):
		is_ebook.append(name.text)
		#is_ebook.append(name.text)#child.xpath('//Format/dimensionValues/item/name/text()')
		#if is_ebook[f] == "eBook":
		if is_ebook[f] == "eBook":
			bool_is_ebook = 1
		else:
			bool_is_ebook = 0
		total_bool_is_ebook += bool_is_ebook
		f += 1
	if total_bool_is_ebook > 0:
		bool_is_ebook = 1
	else:
		bool_is_ebook = 0

def loopThroughInputList():
	global il
	il = 0
	global BNum
	global child
	global collection_short
	
	while il < len(BNums):
		BNum = BNums[il]
		endeca_url = "http://search.lib.unc.edu/search?R=UNC"+BNum+"&output-format=xml&record-options=include-record-facets"
		#webbrowser.open(endeca_url)	# here's your XML file in browser, if you want it.
		urllib.urlretrieve(endeca_url, 'BNum_XMLs/' + BNum + '.xml')	# saves that XML into the XML folder
		
		tree = ET.parse('BNum_XMLs/' + BNum + '.xml')	# set up XML tree to parse
		root = tree.getroot()
		for child in root:	# tells us (and script) what child is
			root.iter()
		
		parseXML()
		
		il += 1
		time.sleep(1.0)

def parseXML():
	global i
	global format_count
	i = 0
	
	isbn_count = int(child.xpath('count(//Syndetics-ISBN/item)'))
	otherauthor_count = int(child.xpath('count(//Other-Authors/item)'))
	primary_url_count = int(child.xpath('count(//Primary-URL/item)'))
	format_count = int(child.xpath('count(//Format/dimensionValues/item)'))
	isEbook()
		
	ice_toc = int(child.xpath('count(//ICE-Chapter-Title)'))
	if ice_toc > 0:
		ice_toc = 1
	#if ice_toc != 0:	# if the tag ICE-Chapter-Title is not absent (that is, it IS present) Bool =1
	#	bool_ice_toc = 1
	#else:	# if the tag is absent, Bool =0
	#	bool_ice_toc = 0
			
	main_author = int(child.xpath('count(//Main-Author)'))
	#if main_author != None:
	#	bool_main_author = 1
	#else:
	#	bool_main_author = 0
			
		#oclc_number = child[1][1][i][2].find('OCLCNumber')
		#if oclc_number != None:
		#	bool_oclc = 1
		#else:
		#	bool_oclc = 0
				
		#upc = child[1][1][i][2].find('UPC')
		#if upc != None:
		#	bool_upc = 1
		#else:
		#	bool_upc = 0
		
		#populateISBN()
		#isbn1SyndTest()
		#time.sleep(0.001)
		#oclcSynTest()
		#upcSynTest()
		#isbn2xSynTest()
			
		#print child[1][1][i][1].text + ", " + str(bool_ice_toc) + ", " + str(bool_main_author) + ", " + str(bool_oclc) + ", " + str(bool_upc) + ", " + str(otherauthor_count) + ", " + str(isbn_count) + ", " + str(primary_url_count) + ", " + str(bool_is_ebook) + ", " + str(isbnx[0]) + ", " + str(bool_isbn1_summary) + ", " + str(bool_isbn1_toc) + ", " + str(bool_isbn1_dbc) + ", " + str(bool_isbn1_lc) + ", " + str(bool_isbn1_mc) + ", " + str(bool_isbn1_sc) + ", " + str(bool_oclc_summary) + ", " + str(bool_oclc_toc) + ", " + str(bool_oclc_dbc) + ", " + str(bool_oclc_lc) + ", " + str(bool_oclc_mc) + ", " + str(bool_oclc_sc) + ", " + str(bool_upc_avsummary) + ", " + str(bool_upc_toc) + ", " + str(bool_upc_dbc) + ", " + str(bool_upc_lc) + ", " + str(bool_upc_mc) + ", " + str(bool_upc_sc) + ", " + str(bool_isbn2x_summary) + ", " + str(bool_isbn2x_toc) + ", " + str(bool_isbn2x_dbc) + ", " + str(bool_isbn2x_lc) + ", " + str(bool_isbn2x_mc) + ", " + str(bool_isbn2x_sc)
		#c.writerow([collection_short, child[1][1][i][1].text, collection_short + child[1][1][i][1].text, bool_ice_toc, bool_main_author, bool_oclc, bool_upc, otherauthor_count, isbn_count, primary_url_count, str(bool_isbn1_summary), str(bool_isbn1_toc), str(bool_isbn1_dbc), str(bool_isbn1_lc), str(bool_isbn1_mc), str(bool_isbn1_sc), str(bool_oclc_summary), str(bool_oclc_toc), str(bool_oclc_dbc), str(bool_oclc_lc), str(bool_oclc_mc), str(bool_oclc_sc), str(bool_upc_avsummary), str(bool_upc_toc), str(bool_upc_dbc), str(bool_upc_lc), str(bool_upc_mc), str(bool_upc_sc), str(bool_isbn2x_summary), str(bool_isbn2x_toc), str(bool_isbn2x_dbc), str(bool_isbn2x_lc), str(bool_isbn2x_mc), str(bool_isbn2x_sc)])
	
	print(BNum, isbn_count, ice_toc, otherauthor_count, primary_url_count, format_count, is_ebook, bool_is_ebook)
	
	i += 1		
		
with open('BNums.txt', 'r') as f:
	BNums = f.read().splitlines()

#c = csv.writer(open("python_output.csv", "wb"))
#c.writerow(["Collection", "UNCb Identifier", "PK", "ICE ToC", "Main Author", "OCLC Number", "UPC", "Other Authors", "Syndetics ISBNs", "Primary URLs", "ISBN1:SUMMARY", "ISBN1:TOC", "ISBN1:DBCHAPTER", "ISBN1:LC", "ISBN1:MC", "ISBN1:SC", "OCLC:SUMMARY", "OCLC:TOC", "OCLC:DBCHAPTER", "OCLC:LC", "OCLC:MC", "OCLC:SC", "UPC:AVSUMMARY", "UPC:TOC", "UPC:DBCHAPTER", "UPC:LC", "UPC:MC", "UPC:SC","ISBN2X:SUMMARY", "ISBN2X:TOC", "ISBN2X:DBCHAPTER", "ISBN2X:LC", "ISBN2x:MC", "ISBN2X:SC", "LC CLASS BOOL", "LCSH COUNT", "MESH COUNT", "OTHER SH COUNT"])

loopThroughInputList()
