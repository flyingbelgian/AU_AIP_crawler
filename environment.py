import os


class Paths:
    def __init__(self):
        self.root_path = os.getcwd()
        self.aerodromes = os.path.join(self.root_path, "aerodromes.csv")
        self.airac = os.path.join(self.root_path, "AIRAC.csv")
        self.subscribers = os.path.join(self.root_path, "subscribers.csv")
        self.path_names = [
            "html_archive",
            "listing_archive",
            "listing_current",
            "pdf_archive",
            "pdf_current",
            "pdf_archive_raw",
            "report_archive",
        ]
        self.path_dict = {}
        for path in self.path_names:
            path_data = self.addPath(path)
            self.path_dict[path_data[0]] = path_data[1]

    def addPath(self, path_name):
        """ Checks to see if required directory exists, creates it if it doesn't exist """
        full_path = os.path.join(self.root_path, path_name)
        if not os.path.isdir(full_path):
            os.mkdir(full_path)
        return [path_name, full_path]

    def archiveFiles(self, current_path, archive_path):
        """ Move files from current folder to an archive folder """
        for file_name in os.listdir(current_path):
            current = os.path.join(current_path, file_name)
            archive = os.path.join(archive_path, file_name)
            os.replace(current, archive)

    def getLatestFile(self, type, airport, path):
        file_list = [file for file in os.listdir(path) if type in file if airport in file]
        if file_list == []:
            print("No relevant file(s) in archive.")
            return "na"
        else:
            file_list.sort(reverse=True)
            file_path = os.path.join(path, file_list[0])
            return file_path
     