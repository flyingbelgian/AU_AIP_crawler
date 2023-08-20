# AU_AIP_crawler
Automatically download updated AU AIP data

Required modules (install these with pip install):
- beautifulsoup4
- csv (no longer required, included with Python install)
- datetime
- os (no longer required, included with Python install)
- PyMuPDF
- requests

USAGE:
- List all aerodromes for which updates are required in aerodromes.csv (1 entry per line)

FUNCTIONS:
Completed:
 - get pdfs combined in single bookmarked pdf, datecode in filename
 - reading csv to process multiple aerodromes
 - get ERSA files for specified aerodromes
 <!-- - generate for csv listing all charts per aerodrome per cycle, datecode in filename
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
 - release v1.0.2 -->

Current phase:
 
Todos:
 <!-- - add counter (current vs total) when downloading files so user has sense of progress
 - allow for checking both current and pending, or choose when running app
 - compare current ERSA pages with last cycle's pages and identify which pages have changed from last cycle
 - fix bookmarks in ERSA pages (currently always shows RDS as page 2 (based on list index))
 - improve formatting of email (especially table listing change, i.e. include html tags)
 - attach copy of changed charts to email -->
