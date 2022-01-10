import datetime as dt
import os
import pandas
import smtplib


class Comparison:
    def __init__(self, type, airport, csv_previous, csv_current, report_path):
        self.airport = airport
        self.type = type
        # Read previous file detail listing and remove unneeded information
        self.list_previous = pandas.read_csv(csv_previous)
        self.list_previous.drop(columns=['File', 'DateFormatted'], inplace=True)
        self.list_previous.set_index('Title', inplace=True)
        # Read current file detail listing and remove unneeded information
        self.list_current = pandas.read_csv(csv_current)
        self.list_current.drop(columns=['File', 'DateFormatted'], inplace=True)
        self.list_current.set_index('Title', inplace=True)
        # Initiate report contents, send email if difference is found
        self.report_lines = []
        if self.getDifference():
            self.sendReport()
        # Save report for current comparison to reports archive
        self.saveReport(report_path)

    def getDifference(self):
        """ Compares current listing with previous listing, populates lines to generate a report """
        """ and returns boolean indicating whether or not a difference was found """
        # Merge previous and current listing
        # filtering out only those entries with different effective dates
        combined_list = self.list_current.merge(
            self.list_previous, on="Title", how='outer').query('Effective_x != Effective_y')
        # Deal with case where there are no differences
        if combined_list.empty:
            self.report_lines.append(
                f"There are no changes in the {self.type} files for {self.airport} this cycle.")
            different = False
        # If differences are found, they are added to report and function set to return True
        else:
            combined_list.fillna("NONE", inplace=True)
            combined_list.rename(columns={
                'Effective_x': 'Previous Cycle',
                'Effective_y': 'Current Cycle'
            }, inplace=True)
            self.report_lines.append(
                "Following files are different between the previous and current ")
            self.report_lines.append(
                f"{self.type} cycles for {self.airport}.\n")
            self.report_lines.append(combined_list.to_string())
            different = True
        self.report_lines.append("\n\n")
        return different

    def saveReport(self, path):
        """ Print report lines to text file in report archive folder """
        date = dt.date.today().strftime("%Y%m%d")
        file_name = f"report{date}.txt"
        file_path = os.path.join(path, file_name)
        with open(file_path, 'a') as report_file:
            for report_line in self.report_lines:
                report_file.write(report_line)

    def sendReport(self):
        """ Send email with report lines to all addressees in subscriber.csv """
        with open('subscribers.csv') as file:
            addressees = file.read().splitlines()
        report_string = "".join(self.report_lines)
        mail_header = f"Subject:Summary of changes for {self.airport} {self.type} files\n\n"
        message = mail_header + report_string
        my_email = 'bru15septest@gmail.com'
        my_password = 'panuy302421'
        connection = smtplib.SMTP('smtp.gmail.com')
        connection.starttls()
        connection.login(user=my_email, password=my_password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=addressees,
            msg=message)
        connection.close()
