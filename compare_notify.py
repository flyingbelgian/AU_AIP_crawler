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
        # self.list_difference = self.list_current.compare(self.list_previous, keep_shape=False)

    def getDifference(self):
        combined_list = self.list_current.merge(self.list_previous, on="Title", how='outer')
        # combined_list = self.list_current
        if combined_list.empty:
            new_line =
            f"There are no changes in the {self.type} files for {self.airport} this cycle."
        else:
            new_line = "Following files are different between the previous and current "
            new_line += f"{self.type} cycles for {self.airport}.\n"
            new_line += combined_list.to_string()
        self.report_lines.append(new_line)
        self.report_lines.append("\n\n")
        if combined_list.empty:
            new_line =
            f"There are no changes in the {self.type} files for {self.airport} this cycle."
        else:
            new_line = "Following files are different between the previous and current "
            new_line += f"{self.type} cycles for {self.airport}.\n"
            new_line += combined_list.to_string()
        self.report_lines.append(new_line)
        self.report_lines.append("\n\n")
        return combined_list
