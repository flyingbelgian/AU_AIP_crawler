from bs4 import BeautifulSoup as bs
import datetime as dt
import pandas


class DAPdata:
    def __init__(self,html,pub_date,airport):
        self.pub_date = pub_date
        with open(html, 'r') as file:
            source_lines = file.readlines()
        relevant = False
        relevant_lines = []
        for line in source_lines:
            if "</table>" in line:
                relevant = False
            if airport in line:
                relevant = True
            if relevant:
                relevant_lines.append(line)
        relevant_lines.append("</table>")
        filename = f"{html[:-5]}_{airport}.html"
        with open(filename, 'w') as file:
            file.writelines(relevant_lines)
        with open(filename, 'r') as file:
            self.relevant_html = file.read()
        self.entries = self.getEntries()

    def getEntries(self):
        entries = []
        self.soup = bs(self.relevant_html, 'html.parser')
        table = self.soup.find('table')
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
    
    def writeDAPcsv(self):
        panda = pandas.DataFrame(self.entries)
        panda.columns = ['Title', 'File', 'Effective', 'DateFormatted']
        panda.to_csv("current_DAP.csv", index=False, )
