Contents:
1. GENERAL INFORMATION
2. USAGE INSTRUCTIONS
3. FILES INCLUDED
4. CONTACT INFORMATION
-----------------------

1.GENERAL INFORMATION

This dataset contains Australian legal cases from the Federal Court of Australia (FCA). The cases were downloaded from AustLII (http://www.austlii.edu.au). We included all files from the year 2006,2007,2008 and 2009.
We built it to experiment with automatic summarization and citation analysis.
For each document we collected catchphrases, citations sentences, citation catchphrases, and citation classes. Catchphrases are found in the document, we used the catchphrases are gold standard for our summarization experiments. Citation sentences are found in later cases that cite the present case, we use citation sentences for summarization. Citation catchphrases are the catchphrases (where available) of both later cases that cite the present case, and older cases cited by the present case. Citation classes are indicated in the document, and indicate the type of treatment given to the cases cited by the present case.
We tried to make the xml format of the file intuitive, it should be no problem understanding how the files are structured.
More informations is given in the FILES INCLUDED section. To understand how the data can be used we suggest to look at:
if you are interested in summarization:
	F. Galgani, P. Compton, and A. Hoffmann. Combining different summarization techniques for legal text. In Proceedings of the Workshop on Innovative Hybrid Approaches to the Processing of Textual Data, pages 115–123, Avignon, France, April 2012. Association for Computational Linguistics.

if you are interested in citation classification:

F. Galgani and A. Hoffmann. Lexa: Towards automatic legal citation classification. In J. Li, editor, AI 2010: Advances in Artificial Intelligence, volume 6464 of Lecture Notes in Computer Science, pages 445 –454. Springer Berlin Heidelberg, 2010.

Or feel free to contact me (galganif@cse.unsw.edu.au) if it is still unclear.


2. USAGE INSTRUCTIONS

To use this data, please follow the following guidelines:

   1. For research only.  
   2. Do not re-distribute.  
   3. If you decide to use this work in your publication, 
   Please cite one of the following papers.

@inproceedings{lexa,
	Affiliation = {School of Computer Science and Engineering, The University of New South Wales, Sydney, Australia},
	Author = {Galgani, Filippo and Hoffmann, Achim},
	Booktitle = {AI 2010: Advances in Artificial Intelligence},
	Date-Added = {2011-05-13 14:42:04 +1000},
	Date-Modified = {2012-01-30 12:55:20 +1100},
	Editor = {Li, Jiuyong},
	Keywords = {legal, citation, rdr},
	Pages = {445 -454},
	Publisher = {Springer Berlin Heidelberg},
	Series = {Lecture Notes in Computer Science},
	Title = {LEXA: Towards Automatic Legal Citation Classification},
	Volume = {6464},
	Year = {2010}}

@inproceedings{cicling12,
	Address = {New Delhi, India},
	Author = {Filippo Galgani and Paul Compton and Achim Hoffmann},
	Booktitle = {the 13th International Conference on Intelligent Text Processing and Computational Linguistics},
	Date-Added = {2012-01-31 15:41:37 +1100},
	Date-Modified = {2012-04-16 13:30:35 +1000},
	Pages = {415--426},
	Publisher = {Springer Berlin Heidelberg},
	Series = {Lecture Notes in Computer Science},
	Title = {Towards automatic generation of catchphrases for legal case reports},
	Volume = {7182},
	Year = {2012}}

@inproceedings{pkaw,
	Author = {Filippo Galgani and Paul Compton and Achim Hoffmann},
	Booktitle = {PKAW 2012},
	Date-Added = {2012-06-29 10:19:06 +1000},
	Date-Modified = {2012-06-29 10:21:12 +1000},
	Editor = {D. Richards and B.H. Kang},
	Pages = {118--132},
	Publisher = {Springer, Heidelberg},
	Title = {Knowledge Acquisition for Categorization of Legal Case Reports},
	Volume = {LNAI 7457},
	Year = {2012}}

@inproceedings{pricai,
	Author = {Filippo Galgani and Paul Compton and Achim Hoffmann},
	Booktitle = {PRICAI 2012},
	Date-Added = {2012-06-29 10:56:27 +1000},
	Date-Modified = {2012-07-04 09:51:37 +1000},
	Pages = {40--52},
	Publisher = {Springer, Heidelberg},
	Title = {Citation Based Summarisation of Legal Texts},
	Volume = {LNCS 7458},
	Year = {2012}}

   4. Please inform us if you publish as we are interested in the
   output of this work.


3. FILES INCLUDED

	Directories:

1. fulltext: Contains the full text and the catchphrases of all the cases from the FCA. Every document (<case>) contains:
	<name> : name of the case
	<AustLII> : link to the austlii page from where the document was taken
	<catchphrases> : contains a list of <catchphrase> elements
		<catchphrase> : a catchphrase for the case, with an id attribute 
	<sentences> : contains a list of <sentence> elements
		<sentence> : a sentence with id attribute

2. citations_summ: Contains citations element for each case. Fields:
	<name> : name of the case
	<AustLII> : link to the austlii page from where the document was taken
	<citphrases> : contains a list of <citphrase> elements
		<citphrase> : a citphrase for the case, this is a catchphrase from a case which is cited or cite the current one. Attributes: id,type (cited or citing),from(the case from where the catchphrase is taken).
	<citances> : contains a list of <citance> elements
		<citance> : a citance for the case, this is a sentence from a later case that mention the current case. Attributes: id,from(the case from where the citance is taken).
	<legistitles> : contains a list of <title> elements	
		<title> : Title of a piece of legislation cited by the current case (can be an act or a specific section).

3. citations_class: Contains for each case a list of labeled citations. Fields:
	<name> : name of the case
	<AustLII> : link to the austlii page from where the document was taken
	<citations> : contains a list of <citation> elements
		<citation> : a citation to an older case, it has an id attribute and contains the following elements:
			<class> : the class of the citation as indicated on the document
			<tocase> : the name of the case which is cited
			<AustLII> : the link to the document of the case which is cited
			<text> : paragraphs in the cited case where the current case is mentioned



4. CONTACT INFORMATION
For any question please email:
Filippo Galgani
galganif@cse.unsw.edu.au
http://www.cse.unsw.edu.au/~galganif