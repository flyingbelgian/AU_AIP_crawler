import os, time

class Paths:
    def __init__(self):
        self.cwd = os.getcwd()
        self.path_names = [
            "html_archive",
            "html_temp",
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

    def addPath(self, path_name):
        """ Checks to see if required directory exists, creates it if it doesn't exist """
        full_path = os.path.join(self.cwd, path_name)
        if not os.path.isdir(full_path):
            os.mkdir(full_path)
        return [path_name,full_path]

    def pathCleanUp(self,temp_path,archive_path):
        """ Move temporary files from a temporary folder to an archive folder """
        """ and delete the temporary folder """
        for file_name in os.listdir(temp_path):
            os.replace(os.path.join(temp_path, file_name), os.path.join(archive_path, file_name))
        os.rmdir(temp_path)

    def finalCleanUp(self):
        """ Cleans up all temporary folders as defined in this method """
        self.pathCleanUp(self.path_dict['html_temp'], self.path_dict['html_archive'])
