# AU_AIP_crawler
 Automatically download updated AU AIP data 

AIRAC.csv includes all airac cycles as currently listed by Eurocontrol (https://www.nm.eurocontrol.int/RAD/common/airac_dates.html). The Australian publication cycle is published here: https://www.airservicesaustralia.com/industry-info/aeronautical-information-management/document-amendment-calendar/ per type of document there is a column which is left empty if there is no publication in that AIRAC cycle, or which contains the cycle designator if their is a publication on that cycle.

Time checks assume an irrelevant time-zone difference in terms of days when the script is run. This means it still works when checking at the start of the work-day when run in UTC+8, but might not work when run in places further west from Australia. (this is handled in the getPublicationDates function in the source.py file)
Datecodes are standardised as YYYYMMDD to allow mathematical evaluation of what data is latest and what is the previous data.

Completed:
- get pdfs combined in single bookmarked pdf, datecode in filename

Current phase:
- move all single pdfs to archive folder for future reference
	Seems to be an issue with the pdf merger not properly closing the files. The last line of cleanup at this stage is supposed to move pdf files from the pdf_temp path to the pdf_raw path, but it generates a windows error saying that the file cannot be moved because it's still open with another process.
    Looked through the output.py to confirm that the file has a .close() line, but that doesn't appear to fix the problem. Adding a 5 second delay to allow processes to finish didn't help either (was a desperate attempt). Will probably need to generate a stackexchange post to ask for help.	

Todos:
- generate for csv listing all charts per aerodrome per cycle, datecode in filename
- compare current chart dates with last cycle's chart dates and identify which charts have changed from last cycle
- send email notifying existence of new combined pdf for each cycle
- email to list which charts have changed
- attach copy of changed charts to email
