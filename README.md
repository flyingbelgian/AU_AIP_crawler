# AU_AIP_crawler
 Automatically download updated AU AIP data

AIRAC.csv includes all airac cycles as currently listed by Eurocontrol (https://www.nm.eurocontrol.int/RAD/common/airac_dates.html). The Australian publication cycle is published here: https://www.airservicesaustralia.com/industry-info/aeronautical-information-management/document-amendment-calendar/ per type of document there is a column which is left empty if there is no publication in that AIRAC cycle, or which contains the cycle designator if their is a publication on that cycle. It is intended to be run with a scheduler to ensure the script regularly checks for new updates (recommended to be at least once per AIRAC cycle).

Time checks assume an irrelevant time-zone difference in terms of days when the script is run. This means it still works when checking at the start of the work-day when run in UTC+8, but might not work when run in places further west from Australia. (this is handled in the getPublicationDates function in the source.py file)
Datecodes are standardised as YYYYMMDD to allow mathematical evaluation of what data is latest and what is the previous data.

Required modules (install these with pip install):
- beautifulsoup4
- csv
- datetime
- os
- pandas
- PyMuPDF
- requests

USAGE:
- Ensure AIRAC.csv is up to date
- List all aerodromes for which updates are required in aerodromes.csv (1 entry per line)
- List all email address that should receive an alert for updated files in subscribers.csv (1 entry per line)
- Ensure proper folder is set in environment.py, the folder will be the location where files are stored and where the script will look for the AIRAC, aerodromes and subscriber csvs.

FUNCTIONS:
Completed:
 - get pdfs combined in single bookmarked pdf, datecode in filename
 - reading csv to process multiple aerodromes
 - get ERSA files for specified aerodromes
 - generate for csv listing all charts per aerodrome per cycle, datecode in filename
 - check if source pdf already exist to save on download bandwidth
 - archive files in current... directories to archive prior to creating new files
 - compare current DAP chart dates with last cycle's chart dates and identify which charts have changed from last cycle
 - send email notifying existence of new/removed/modified DAP charts for each cycle
 - release first v1.0.0
 - made allowances for files and parameters to be stored in folder other than script root
 - release v1.0.1
 - script can run independent of location (reads cwd to find related files)
 - added counter showing filenames as they're being downloaded
 - disabled email notification due to problem with automated gmail login
 - fixed list index error when no previous files exist for an AD
 - release v1.0.2

Current phase:
 
Todos:
 - add counter (current vs total) when downloading files so user has sense of progress
 - allow for checking both current and pending, or choose when running app
 - compare current ERSA pages with last cycle's pages and identify which pages have changed from last cycle
 - fix bookmarks in ERSA pages (currently always shows RDS as page 2 (based on list index))
 - improve formatting of email (especially table listing change, i.e. include html tags)
 - attach copy of changed charts to email
