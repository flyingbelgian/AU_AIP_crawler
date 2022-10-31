import requests as req
import datetime as dt
from bs4 import BeautifulSoup as bs
import pandas
import csv

currentDate = dt.date.today().strftime("%Y%m%d")

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

### Generates a csv named active_links.csv containing currently available source
### on the AIP website top level page.
print(f"Getting content from AIP top level site.")
mainURL = "https://www.airservicesaustralia.com/aip/aip.asp?pg=10"
source = getSource(mainURL)
output = []
AIP_full_file = f"html_archive/{currentDate}_AIP_full.html"
with open (AIP_full_file, 'w') as file:
    file.write(source.text)
with open (AIP_full_file, 'r') as file:
    source_lines = file.readlines()
    relevant_lines = []
    for line in source_lines:
        if "<li><a href=" in line:
            if "!--" in line:
                pass
            else:
                relevant_lines.append(line)
AIP_filtered_file = f"html_archive/{currentDate}_AIP_filtered.html"
with open (AIP_filtered_file, 'w') as file:
    file.write("<ul>")
    file.write("\n")
    for line in relevant_lines:
        str = line
        if str[-6:-1] != "</li>":
            str = str[:-1] + "</li>" + str[-1:]
        file.write(str)
    file.write("</ul>")
with open (AIP_filtered_file, 'r') as file:
    soup = bs(file, 'html.parser')
    for line in soup.find_all('a'):
        link = line.get('href')
        type = line.string.replace(","," -")
        date = line.next_sibling
        unwanted_characters = (" ", "(", ")")
        if date != None:
            for i in unwanted_characters:
                date = date.replace(i,"")
        else:
            date = ""
        output.append((link,type,date))
AIP_links_file = f"source_current/{currentDate}_AIP_links.csv"
with open (AIP_links_file, 'w') as file:
    for item in output:
        file.writelines(f"{item[0]},{item[1]},{item[2]}\n")

### Generates a CSV named DAP_links.csv containing currently available DAP cycles
### with link extensions and dates
DAPcycles = []
with open (AIP_links_file, 'r') as file:
    links = file.readlines()
    for line in links:
        if "(DAP)" in line:
            relevant_line = line[:-1].split(",")
            DAPcycles.append(relevant_line)
            print(f"Found DAP dated {relevant_line[2]}")

### Generates a CSV named ERSA_links.csv containing currently available DAP cycles
### with link extensions and dates
ERSAcycles = []
with open (AIP_links_file, 'r') as file:
    links = file.readlines()
    for line in links:
        if "(ERSA)" in line:
            relevant_line = line[:-1].split(",")
            ERSAcycles.append(relevant_line)
            print(f"Found ERSA dated {relevant_line[2]}")

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

