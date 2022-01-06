import os


class Paths:
    def __init__(self):
        self.cwd = os.getcwd()
        self.path_names = [
            "html_archive",
            "listing_archive",
            "listing_current",
            "pdf_archive",
            "pdf_current",
            "pdf_archive_raw",
        ]
        self.path_dict = {}
        for path in self.path_names:
            path_data = self.addPath(path)
            self.path_dict[path_data[0]] = path_data[1]

    def archiveFiles(self, current_path, archive_path):
        """ Move files from current folder to an archive folder """
        for file_name in os.listdir(current_path):
            current = os.path.join(current_path, file_name)
            archive = os.path.join(archive_path, file_name)
            os.replace(current, archive)

    def addPath(self, path_name):
        """ Checks to see if required directory exists, creates it if it doesn't exist """
        full_path = os.path.join(self.cwd, path_name)
        if not os.path.isdir(full_path):
            os.mkdir(full_path)
        return [path_name, full_path]
