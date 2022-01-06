import datetime as dt
import requests as req
import csv, os

class Source:
    source_date = dt.date.today().strftime("%Y%m%d") # Current date when source is acquired

    def getSource(self,url):
        '''Uses headers and data entries to access airservices website and retrieve the requested information'''
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
        response = req.get(url, headers=headers, data=data)
        return response

class HTML(Source):
    def getPubDateCycle(self,column):
        '''Retrieves the relevant publication date of the source, based on current time and published publication schedule'''
        '''See readme.md for more information'''
        with open("AIRAC.csv", 'r') as file:
            airac_dates = csv.reader(file)
            next(airac_dates)
            for row in airac_dates:
                if int(row[1]) < int(self.source_date) and row[column] != '':
                    self.pub_date = str(row[1])
                    self.pub_cycle = str(row[column])

    def saveSource(self,path):
        filename = f"{self.pub_date}_{self.type}_{self.pub_cycle}.html"
        self.html = os.path.join(path,filename)
        if filename in os.listdir(path):
            pass
        else:
            response = self.getSource(self.url)
            with open(self.html, 'w', encoding="utf-8") as file:
               file.write(response.text)

class DAPhtml(HTML):
    def __init__(self,path):
        self.path = path
        self.type = "DAP"
        self.pub_cycle_column = 5
        self.getPubDateCycle(self.pub_cycle_column)
        self.url = "https://www.airservicesaustralia.com/aip/current/dap/AeroProcChartsTOC.htm"
        self.saveSource(self.path)

class DAPfile(Source):
    def __init__(self,path,filename):
        if filename in os.listdir(path):
            pass
        else:
            url = f"https://www.airservicesaustralia.com/aip/current/dap/{filename}"
            response = self.getSource(url)
            filepath = os.path.join(path, filename)
            with open(filepath, 'wb') as file:
              file.write(response.content)

class ERSAhtml(HTML):
    def __init__(self,path):
        self.type = "ERSA"
        self.pub_cycle_column = 4
        self.getPubDateCycle(self.pub_cycle_column)
        self.url = f"https://www.airservicesaustralia.com/aip/aip.asp?pg=40&vdate={self.pub_cycle}&ver=1"
        self.saveSource(path)

class ERSAfile(Source):
    def __init__(self,path,filename):
        if filename in os.listdir(path):
            pass
        else:
            url = f"https://www.airservicesaustralia.com/aip/current/ersa/{filename}"
            response = self.getSource(url)
            filepath = os.path.join(path, filename)
            with open(filepath, 'wb') as file:
              file.write(response.content)
