import datetime as dt
from dateutil.parser import parse
import logging as log
import os
import re
import requests as req

currentDate = dt.date.today().strftime("%Y%m%d")

### Setup log file, opening it once to ensure an empty log file on each run
logfile = f"log_source_{currentDate}.txt"
with open(logfile, 'w'):
    pass
log.basicConfig(filename=logfile, level=log.DEBUG)

def getSource(url):
    ### Gets URL contents after passing through the mandatory gateway on the AIP website
    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Microsoft Edge";v="96"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Origin': 'https://www.airservicesaustralia.com',
        'Upgrade-Insecure-Requests': '1',
        'DNT': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Referer': 'https://www.airservicesaustralia.com/aip/aip.asp',
        'Accept-Language': 'en-US,en;q=0.9,id;q=0.8,nl;q=0.7,fr;q=0.6',
    }
    data = {
        'Submit': 'I Agree',
        'check': '1'
    }
    return req.get(url, headers=headers, data=data)

rootURL = "https://www.airservicesaustralia.com/aip/"

### Generates a list of lines containing links on the AIP website top level page.
print(f"Getting content from AIP top level site.")
AIP_URL = "aip.asp?pg=10"
AIP_src_raw = getSource(f"{rootURL}{AIP_URL}").text
AIP_source_lines = AIP_src_raw.splitlines()
AIP_relevant_lines = []
for line in AIP_source_lines:
    ### Record only list items that have href in them, which aren't disabled by !-- prefix
    if "<li><a href=" in line:
        if "!--" in line:
            pass
        else:
            AIP_relevant_lines.append(line)
AIP_link_data = []
for line in AIP_relevant_lines:
    ### Extracts types, dates and links from list of lines on AIP website top level page.
    relevantparts = re.split(r'<a href="|">|</a>|</li>', line)
    AIP_link = relevantparts[1].replace("&amp;","&")
    AIP_type = relevantparts[2]
    try:
        AIP_date = parse(relevantparts[3], fuzzy=True).date()
    except:
        AIP_date = ""
    AIP_link_data.append({"link":AIP_link, "type":AIP_type, "date":AIP_date})
### Debugging info printed to logfile
log.debug(f"Identified {len(AIP_link_data)} AIP types - dates - links:")
for data in AIP_link_data:
    log.debug(f" - {data['type']} - {data['date']} - {data['link']}")

#################### DAP ####################
### Identifies currently available DAP cycles
DAP_menu_links = []
for data in AIP_link_data:
    if "(DAP)" in data['type']:
        print(f"Found DAP listing for {data['date']}")
        DAP_menu_html = getSource(f"{rootURL}{data['link']}").text
        for line in DAP_menu_html.splitlines():
            if "Charts" in line:
                DAP_listing_link = rootURL + line.split('href="',1)[1].split('">',1)[0]
                DAP_listing_html = getSource(DAP_listing_link)
                DAP_cycle = DAP_listing_html.text.split("DAP ",1)[1].split(" - ",1)[0]
                DAP_menu_links.append({
                    "link":DAP_listing_link,
                    "date":data['date'],
                    "cycle":DAP_cycle,
                    "html":DAP_listing_html
                    })
### Debugging info printed to logfile
log.debug(f"Identified {len(DAP_menu_links)} DAP listing links:")
for item in DAP_menu_links:
    log.debug(f" - {item['date']} - {item['cycle']} - {item['link']}")
###

def getDAPfiles(airport):
    ### Downloads all DAP files for a given aerodrome
    log.getLogger('chardet').propagate = False
    os.chdir("pdf_archive_raw")
    DAP_file_listings = [] # Track cycles with their file listings
    for DAP_menu_link in DAP_menu_links:
        ### Downloads all files from each of the links found
        print(f"Downloading DAP files for {airport} in DAP {DAP_menu_link['cycle']}", end=" ")
        print(f"dated {DAP_menu_link['date']}")
        DAPcycle_files = [] # Track all files downloaded per cycle
        DAPcycle_URLroot = DAP_menu_link['link'].split("AeroProcChartsTOC")[0]
        all_lines = DAP_menu_link['html'].text.splitlines()
        relevant_lines = []
        relevant = False
        for line in all_lines:
            ### Start recording lines when airport is mentioned, turn off when next airport starts
            if airport in line:
                relevant = True
            else:
                if "text-align" in line: # Heading for next airport listing has "text-align" in it
                    relevant = False
            ### Retain only those lines from previous filter that have a link in them
            if (relevant and "href" in line):
                relevant_lines.append(line)
        for line in relevant_lines:
            ### Read description and filename from relevant lines
            name = line.split("pdf>")[1].split("</a>")[0]
            file = line.split("<a href=")[1].split(">")[0]
            url = DAPcycle_URLroot + file
            DAPcycle_files.append({"name":name, "file":file, "url":url})
        DAP_filecount = 1
        for DAPcycle_file in DAPcycle_files:
            print(f"  {DAP_filecount}/{len(DAPcycle_files)} : {DAPcycle_file['file']} - ", end="")
            if DAPcycle_file["file"] in os.listdir():
                print("Existing File")
                pass
            else:
                print("Downloading ... ", end="")
                response = getSource(DAPcycle_file["url"])
                with open(DAPcycle_file["file"], 'w', encoding="utf-8") as file:
                    file.write(response.text)
                print("Done")
            DAP_filecount += 1
        DAP_file_listings.append({
            "DAPcycle":DAP_menu_link["cycle"],
            "DAPcycle_files":DAPcycle_files
            })
    log.getLogger('chardet').propagate = True
    os.chdir("../")
    return DAP_file_listings

#################### ERSA ####################
# ### Generates a CSV named ERSA_links.csv containing currently available DAP cycles
# ### with link extensions and dates
# ERSAcycles = []
# with open (AIP_links_file, 'r') as file:
#     links = file.readlines()
#     for line in links:
#         if "(ERSA)" in line:
#             relevant_line = line[:-1].split(",")
#             ERSAcycles.append(relevant_line)
#             print(f"Found ERSA dated {relevant_line[2]}")

# def getDAPcontent(date):
#     class HTML(Source):
#     def getPubDateCycle(self, airac, column):
#         # Retrieves the relevant publication date of the source, based on current time and published publication schedule
#         # See readme.md for more information'''
#         for row in airac:
#             if int(row[1]) < int(self.source_date) and row[column] != '':
#                 self.current_date = str(row[1])
#                 self.current_cycle = str(row[column])
#         for row in reversed(airac):
#             if int(row[1]) > int(self.source_date) and row[column] != '':
#                 self.pending_date = str(row[1])
#                 self.pending_cycle = str(row[column])

#     def saveSource(self, path):
#         filename = f"{self.current_date}_{self.type}_{self.current_cycle}.html"
#         self.html = os.path.join(path, filename)
#         if filename in os.listdir(path):
#             pass
#         else:
#             response = self.getSource(self.url)
#             if response.status_code == 404:
#                 print(f"{filename} doesn't exist on server")
#             else:
#                 with open(self.html, 'w', encoding="utf-8") as file:
#                     file.write(response.text)


# class DAPhtml(HTML):
#     def __init__(self, airac, path):
#         self.path = path
#         self.type = "DAP"
#         self.pub_cycle_column = 5
#         self.getPubDateCycle(airac, self.pub_cycle_column)
#         self.url = "https://www.airservicesaustralia.com/aip/current/dap/AeroProcChartsTOC.htm"
#         self.saveSource(self.path)


# class DAPfile(Source):
#     def __init__(self, path, filename):
#         if filename in os.listdir(path):
#             pass
#         else:
#             url = f"https://www.airservicesaustralia.com/aip/current/dap/{filename}"
#             response = self.getSource(url)
#             filepath = os.path.join(path, filename)
#             with open(filepath, 'wb') as file:
#                 file.write(response.content)
#             print(f">> {filename}")

