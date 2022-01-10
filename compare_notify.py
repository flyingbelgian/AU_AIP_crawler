import pandas


class Comparison:
    def __init__(self, type, airport, csv_previous, csv_current):
        self.airport = airport
        self.type = type
        self.list_previous = pandas.read_csv(csv_previous)
        self.list_previous.drop(columns=['File', 'DateFormatted'], inplace=True)
        self.list_previous.set_index('Title', inplace=True)
        # print(self.list_previous)
        self.list_current = pandas.read_csv(csv_current)
        self.list_current.drop(columns=['File', 'DateFormatted'], inplace=True)
        self.list_current.set_index('Title', inplace=True)
        # print(self.list_current)
        self.report_lines = []
        self.getDifference()
        self.appendReport()

    def getDifference(self):
        combined_list = self.list_current.merge(self.list_previous, on="Title", how='outer')
        print(combined_list)
        if combined_list.empty:
            self.report_lines.append(
                f"There are no changes in the {self.type} files for {self.airport} this cycle.")
        else:
            self.report_lines.append(
                "Following files are different between the previous and current ")
            self.report_lines.append(
                f"{self.type} cycles for {self.airport}.\n")
        self.report_lines.append("\n\n")

    def appendReport(self):
        with open("report.txt", 'a') as report_file:
            for report_line in self.report_lines:
                report_file.write(report_line)
