from bs4 import BeautifulSoup as bs
import datetime as dt
import pandas
import os


class HTMLtoCSV:
    def __init__(self, type, html_source, current_path, pub_date, airport):
        self.pub_date = pub_date
        self.airport = airport
        self.html = self.getHTML(html_source)
        self.entries = self.getEntries()
        self.panda = self.getPanda()
        self.writeDAPcsv(current_path, type)

    def getPanda(self):
        panda = pandas.DataFrame(self.entries)
        panda.columns = ['Title', 'File', 'Effective', 'DateFormatted']
        return panda

    def writeDAPcsv(self, current_path, type):
        filename = os.path.join(current_path, f"{self.airport}_{type}_{self.pub_date}.csv")
        self.panda.to_csv(filename, index=False, )


class DAPdata(HTMLtoCSV):
    def getHTML(self, html_source):
        with open(html_source, 'r') as file:
            source_lines = file.readlines()
        relevant = False
        relevant_lines = []
        for line in source_lines:
            if "</table>" in line:
                relevant = False
            if self.airport in line:
                relevant = True
            if relevant:
                line = line.replace("&#47", "/")
                relevant_lines.append(line)
        relevant_lines.append("</table>")
        filename = f"{html_source[:-5]}_{self.airport}.html"
        with open(filename, 'w') as file:
            file.writelines(relevant_lines)
        with open(filename, 'r') as file:
            relevant_html = file.read()
        return relevant_html

    def getEntries(self):
        entries = []
        soup = bs(self.html, 'html.parser')
        table = soup.find('table')
        for tr in table.find_all("tr"):
            entry = []
            for td1 in tr.find_all("td"):
                for td2 in td1.find_all("td"):
                    entry.append(td2.text)
                    link = td2.a
                    if link:
                        entry.append(link['href'])
            entries.append(entry)
        for entry in entries:
            raw_date = entry[2][:-9]
            if len(raw_date) < 11:
                raw_date = "0" + raw_date
            date = dt.datetime.strptime(raw_date, '%d-%b-%Y').date()
            entry.append(date.strftime("%Y%m%d"))
        return entries


class ERSAdata(HTMLtoCSV):
    def getHTML(self, html_source):
        with open(html_source, 'r') as file:
            source_lines = file.readlines()
        relevant_lines = []
        for line in source_lines:
            if f"_{self.airport}_" in line:
                line = line.replace("&#47", "/")
                relevant_lines.append(line)
        filename = f"{html_source[:-5]}_{self.airport}.html"
        with open(filename, 'w') as file:
            file.writelines(relevant_lines)
        with open(filename, 'r') as file:
            relevant_html = file.read()
        return relevant_html

    def getEntries(self):
        entries = []
        soup = bs(self.html, 'html.parser')
        for line in soup.find_all("a"):
            title = line.text
            link = line['href'].split('/')[4]
            effective = link[-13:-4]
            effective_date = dt.datetime.strptime(effective, '%d%b%Y').date()
            date_formatted = effective_date.strftime("%Y%m%d")
            entries.append([title, link, effective, date_formatted])
        return entries
