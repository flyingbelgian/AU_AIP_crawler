# AU_AIP_crawler
 Automatically download updated AU AIP data

AIRAC.csv includes all airac cycles as currently listed by Eurocontrol (https://www.nm.eurocontrol.int/RAD/common/airac_dates.html). The Australian publication cycle is published here: https://www.airservicesaustralia.com/industry-info/aeronautical-information-management/document-amendment-calendar/ per type of document there is a column which is left empty if there is no publication in that AIRAC cycle, or which contains the cycle designator if their is a publication on that cycle.

Time checks assume an irrelevant time-zone difference in terms of days when the script is run. This means it still works when checking at the start of the work-day when run in UTC+8, but might not work when run in places further west from Australia. (this is handled in the getPublicationDates function in the source.py file)
Datecodes are standardised as YYYYMMDD to allow mathematical evaluation of what data is latest and what is the previous data.

Completed:
- get pdfs combined in single bookmarked pdf, datecode in filename
- reading csv to process multiple aerodromes
- get ERSA files for specified aerodromes
- generate for csv listing all charts per aerodrome per cycle, datecode in filename
- check if source pdf already exist to save on download bandwidth
- archive files in current... directories to archive prior to creating new files

Current phase:
- compare current chart dates with last cycle's chart dates and identify which charts have changed from last cycle

Todos:
- send email notifying existence of new combined pdf for each cycle
- email to list which charts have changed
- attach copy of changed charts to email
