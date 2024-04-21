import datetime as dt
from dateutil.parser import parse
import logging as log
import os
import re
import requests as req

currentDate = dt.date.today().strftime("%Y%m%d")

### Setup log file, opening it once to ensure an empty log file on each run
logfile = f"log_source_{currentDate}.log"
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
    try:
        response = req.get(url, headers=headers, data=data)
    except req.exceptions.ConnectionError:
        response = req.get(url, headers=headers, data=data)
    return response

rootURL = "https://www.airservicesaustralia.com/aip/"

### Generates a list of lines containing links on the AIP website top level page.
print(f"Getting listings from AIP top level site.")
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
### Identifies currently available DAP cycles and generates list of links to each cycle's file listing
DAP_menu_links = []
DAP_count = 1
for data in AIP_link_data:
    if "(DAP)" in data['type']:
        print(f"Found DAP listing for {data['date']}")
        # DAP_menu_html = getSource(f"{rootURL}{data['link']}").text
        # f = open("DAP_menu_html.txt","w")
        # f.write(DAP_menu_html)
        # f.close()
        # with open ("DAP_menu_html.txt","r") as file:
        #     content = file.read()
        #     for line in content.splitlines():
        #         # print(line)
        #         if "Charts" in line:
        #             DAP_listing_link = rootURL + line.split('href="',1)[1].split('">',1)[0]
        #             DAP_listing_html = getSource(DAP_listing_link)
        #             DAP_cycle = DAP_listing_html.text.split("DAP ",1)[1].split(" - ",1)[0]
        #             DAP_menu_links.append({
        #                 "link":DAP_listing_link,
        #                 "date":data['date'],
        #                 "cycle":DAP_cycle,
        #                 "html":DAP_listing_html
        #                 })
        DAP_listing_link = rootURL
        if DAP_count == 1:
            DAP_listing_link += "current/dap/"
        elif DAP_count == 2:
            DAP_listing_link += "pending/dap/"
        else:
            print("Invalid DAP count")
            quit()
        DAP_listing_html = getSource(rootURL+data['link'])
        log.debug(DAP_listing_html)
        DAP_cycle =  DAP_listing_html.text.split("DAP ",1)[1].split(" - ",1)[0]
        DAP_menu_links.append({
            "link":DAP_listing_link,
            "date":data['date'],
            "cycle":DAP_cycle,
            "html":DAP_listing_html
            })
        DAP_count += 1
### Debugging info printed to logfile
log.debug(f"Identified {len(DAP_menu_links)} DAP listing links:")
for item in DAP_menu_links:
    log.debug(f" - {item['date']} - {item['cycle']} - {item['link']}")
###

def getDAPfiles(airport):
    ### Downloads all DAP files for a given aerodrome and generates list of files in each cycle
    ### Returns library with cycle number and file library for each cycle
    os.chdir("pdf_archive_raw")
    DAP_file_listings = [] # Track cycles with their file listings
    for DAP_menu_link in DAP_menu_links:
        print(f"Downloading DAP files for {airport} in DAP {DAP_menu_link['cycle']}", end=" ")
        print(f"dated {DAP_menu_link['date']}")
        ### Prepare file for tracking file changes between DAP cycles
        changed_files=open(f"../pdf_latest/{airport}_DAP{DAP_menu_link['cycle']}_changes.txt", 'a')
        changed_files.write(f"Following files changed in DAP{DAP_menu_link['cycle']} cycle:\n")
        ###
        DAPcycle_URLroot = DAP_menu_link['link'].split("AeroProcChartsTOC")[0]
        log.debug(f"DAPcycle URL root: {DAPcycle_URLroot}")
        ### Generate list of files to be downloaded per cycle
        DAPcycle_files = []
        all_lines = DAP_menu_link['html'].text.splitlines()
        relevant_lines = []
        relevant = False
        for line in all_lines:
            if airport in line:
                # Start recording all lines from when airport is first mentioned
                relevant = True
                log.debug(f"Start of relevant lines for {airport} DAP links: {line}")
            else:
                # Stop recording at first mention of next airport
                # Heading for next airport listing has "text-align" in it
                if "text-align" in line:
                    relevant = False
                    # log.debug(f"Stop of relevant lines for {airport} DAP links: {line}")
            # Retain only those lines from previous filter that have a link in them
            if (relevant and "href" in line):
                relevant_lines.append(line)
                log.debug(f"Relevant lines added: {line}")
        for line in relevant_lines:
            # Read description, filename and url from relevant lines
            # Test for quotation marks in href block
            if 'href="' in line:
                quotes='"'
            else:
                quotes=''
            name = line.split(f'.pdf{quotes}>')[1].split("</a>")[0]
            file = line.split(f'href={quotes}')[1].split(f'{quotes}>')[0]
            url = DAPcycle_URLroot + file
            # Store information as library in list of files to be downloaded
            DAPcycle_files.append({
                "name":name,
                "file":file,
                "url":url
                })
        ### Download all the files in the list of files to be downloaded
        DAP_filecount = 1 # Ticker to track number of files downloaded against total
        for DAPcycle_file in DAPcycle_files:
            print(f"  {DAP_filecount}/{len(DAPcycle_files)} : {DAPcycle_file['file']} - ", end="")
            if DAPcycle_file["file"] in os.listdir():
                print("Existing File", end='')
                pass
            else:
                log.debug(f"Downloading {DAPcycle_file['url']}")
                response = getSource(DAPcycle_file["url"])
                with open(DAPcycle_file["file"], 'wb') as file:
                    file.write(response.content)
                print("Downloaded", end='')
            if DAP_menu_link['cycle'] in DAPcycle_file['file']:
                changed_files.write(f" > {DAPcycle_file['file']} - {DAPcycle_file['name']}\n")
                print(' - New File added to list of changes for this cycle')
            else:
                print('')
            DAP_filecount += 1
        changed_files.close()
        DAP_file_listings.append({
            "cycle":DAP_menu_link["cycle"],
            "date":DAP_menu_link["date"],
            "files":DAPcycle_files
            })
    os.chdir("../")
    return DAP_file_listings

#################### ERSA ####################
### Identifies currently available ERSA cycles and generates list of links to each cycle's file listing
ERSA_menu_links = []
for data in AIP_link_data:
    if "(ERSA)" in data["type"]:
        print(f"Found ERSA listing for {data['date']}")
        ERSA_listing_link = rootURL + data['link']
        ERSA_date = data['date']
        ERSA_menu_links.append({
            "link":ERSA_listing_link,
            "date":ERSA_date,
            })
### Debugging info printed to logfile
log.debug(f"Identified {len(ERSA_menu_links)} ERSA listing links:")
for item in ERSA_menu_links:
    log.debug(f" - {item['date']} - {item['link']}")
###

def getERSAfiles(airport):
    ### Downloads all ERSA files for a given aerodrome and generates list of files in each cycle
    ### Returns list with cycle dates and file listings
    os.chdir("pdf_archive_raw")
    ERSA_file_listings = [] # Track cycles with their file listings
    for ERSA_menu_link in ERSA_menu_links:
        ### Downloads all files from each of the links found
        print(f"Downloading ERSA files for {airport} dated {ERSA_menu_link['date']}")
        ERSAcycle_files = [] # Track all files downloaded per cycle
        ERSAcycle_URLroot = rootURL[:-5]
        all_lines = getSource(ERSA_menu_link['link']).text.splitlines()
        relevant_lines = []
        for line in all_lines:
            ### Records all lines that have the airport mentioned in them
            if airport in line:
                relevant_lines.append(line)
        for line in relevant_lines:
            ### Read type and filename from relevant lines
            name = line.split('pdf">')[1].split("</a>")[0]
            link = line.split('<a href="')[1].split('">')[0]
            url = ERSAcycle_URLroot + link
            file = link.split('ersa/')[1].split('"')[0]
            ERSAcycle_files.append({"name":name, "file":file, "url":url})
        ERSA_filecount = 1
        for ERSAcycle_file in ERSAcycle_files:
            print(f"  {ERSA_filecount}/{len(ERSAcycle_files)} : {ERSAcycle_file['file']} - ", end="")
            if ERSAcycle_file["file"] in os.listdir():
                print("Existing File")
                pass
            else:
                log.debug(f"Downloading {ERSAcycle_file['url']}")
                response = getSource(ERSAcycle_file["url"])
                with open(ERSAcycle_file["file"], 'wb') as file:
                    file.write(response.content)
                print("Downloaded")
            ERSA_filecount += 1
        ERSA_file_listings.append({
            "date":ERSA_menu_link["date"],
            "files":ERSAcycle_files
            })
    os.chdir("../")
    return ERSA_file_listings