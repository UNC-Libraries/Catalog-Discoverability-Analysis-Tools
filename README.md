# E-collections discovery evaluation: catalog data
This suite of scripts is used to gather data on the discoverability (in our main online catalog) of individual titles within collections. The output of the scripts is at the individual title (i.e. bibliographic record) level. The script output is ingested into a database used to compile collection-level reports. 

## Questions this is intended to answer for each collection: 
* How many titles are represented by MARC records are in the catalog?
  * This number is to be compared with the number of titles the content provider says we should have
  * We cannot assume/expect exactly matching numbers here due to the existence of multi-volume (or multi-"CD", etc.) e-items and inconsistency in how these are represented, both in MARC records and provider title lists.
* Given the current catalog user interface configuration, how many titles display supplemental content from SyndeticsSolutions at load time: book cover image, table of contents, summary, first chapter, etc.? 
  * How much does this number increase if we change the catalog user interface configuration to send additional match points for each title? 
* How many titles have *indexed, searchable* table of contents data from Syndetics (ICE data) available in the catalog? 
* How many titles have standard classification numbers assigned? LCSH and MeSH are counted.
* What is the richness of the author and standardized subject access points in the records?

# Usage
## Overview of steps
1. Prepare collection list -- this is a tab-delimited text file, with one collection per line.
2. Run the first script with the collection list as input. This produces a list of unsuppressed (i.e. viewable in the public catalog) bib records on which to gather data.
3. Run the second script on the bib record list. This gets some pieces of data that can only be grabbed from the ILS versions of the records. 
4. Run the third script on the bib/ILS data list. This pulls in the data that can only be grabbed by examining the live public catalog records, or querying the Syndetics API. 
5. Import results of the third script into the database to compile collection-level stats/reports.

## Steps in detail
### Prepare collection list
* Format: tab-delimited text file
* File extension: .txt
* Line endings: Unix
* Data
  * Element 1: Collection name to search on in the catalog. See below for more details on this.
  * Element 2: A brief "shortcut" code for the collection. This is used instead of the full collection title string in the database to collapse the individual records into the correct collections, and to create a "this-record-in-this-collection" key, since some records will be part of more than one collection. 

#### More on collection name
* This will be the "Host Item" title (or part of it) that appears in the 773 field in bib records for e-resource collections that are processed by AAL/E-Resources Cataloging. These are the titles that include "(online collection)".
* The query built with the collection name as entered will be a left-anchored phrase match
* The type of query, combined with the structure/design of the assigned collection titles means that we can control the granularity of our reporting by how we enter the collection titles. Example: 
  * This would retrieve all the ACS Symposium Series titles: ACS symposium series (online collection)
  * This would retrieve just the ACS titles in the 2015 collection: ACS symposium series (online collection). 2015
  * This would retrieve all the ACS titles from 2011-2015 collections: ACS symposium series (online collection). 201 *(Note that this wouldn't include titles from the ACS 2010 collection because those were included in the same purchase as the backfile (1949-2009), and so they use the collection title: ACS symposium series (online collection). 1949-2010)*
  * You would NOT want to search on the following, because it could cause collection-level or database records to be pulled into your results, or possibly even print records: ACS symposium series
* UNC staff can look up the 773-field collection titles for all e-resource collections. Instructions on how to access and use this data are here: https://intranet.lib.unc.edu/wikis/staff/index.php/E-Resources_collection_data

### Run first script -- ecoll_catalog_eval_1.pl
The collection list is used as input. Running the script produces a list of unsuppressed (i.e. viewable in the public catalog) bib records on which to gather further data.

This script is a Perl script running on the library server because it needs to interact directly with the ILS database. 

* First move the collection list to the server.
* Run the script like: 

```
perl ecoll_catalog_eval_1.pl path/to/collection_list_file.txt
```

* The output will be written to directory where your collection list file was found. It will be named the same thing as the collection list, with "_bibs" appended, and the file extension changed to .csv: 

```
path/to/collection_list_file_bibs.csv
```

* Before it exits, the script outputs to the screen the total number of records it identified. This should correspond to the number of lines in the output file. If you are evaluating a very large number of collections or some very large collections, you may want to split the output file created by this script into smaller files of <200,000 lines. The subsequent scripts would then be run on the smaller files. 

### Run second script -- ecoll_catalog_eval_2.pl
The output from ecoll_catalog_eval_1.pl is used as input. Running the script gathers data on presence of LC classification number and number of subject headings from the ILS. 

Because this data has to come from the ILS, this is another Perl script running on the library server. 

* Assuming that the output from the first script has been left in place: 

```
perl ecoll_catalog_eval_2.pl path/to/collection_list_file_bibs.csv
```

* The output will be written to: 

```
path/to/collection_list_file_ils.csv
```

### Run third script
For each record listed in the output from the 2nd script, this script grabs data from: 
* the Endeca XML web services API for the full record view
* a series of calls to the Syndetics API

Format for the Endeca full record XML: 

http://search.lib.unc.edu/search?R=UNC{{BNUM}}&output-format=xml&record-options=include-record-facets

URL format for the Syndetics API:

http://syndetics.com/index.aspx?isbn={{ISBN}}&oclc={{OCLCnumber}}&upc={{UPC}}/XML.XML&client=ncchapelh

The script parses the XML of the Endeca XML web services API to find identifiers (ISBNs, OCLC number, UPC) that can be used to construct a URL for the Syndetics API. The script then parses the Syndetics XML to determine what kind of data is and is not returned. Results are appended to the .CSV file created by the second script.

The resulting .CSV can then be analyzed in Microsoft Excel or imported into a Microsoft Access database.
