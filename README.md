# AU_AIP_crawler
 Automatically download updated AU AIP data 

AIRAC.csv includes all airac cycles as currently listed by Eurocontrol (https://www.nm.eurocontrol.int/RAD/common/airac_dates.html). The Australian publication cycle is published here: https://www.airservicesaustralia.com/industry-info/aeronautical-information-management/document-amendment-calendar/ per type of document there is a column which is left empty if there is no publication in that AIRAC cycle, or which contains the cycle designator if their is a publication on that cycle.

Time checks assume an irrelevant time-zone difference in terms of days when the script is run. This means it still works when checking at the start of the work-day when run in UTC+8, but might not work when run in places further west from Australia. (this is handled in the getPublicationDates function in the source.py file)

