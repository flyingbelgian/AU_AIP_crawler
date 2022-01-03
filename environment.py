import os

class Paths:
    def __init__(self):
        self.cwd = os.getcwd()
        paths = [
            "html_archive",
            "html_temp",
            "listing_archive",
            "listing_current",
            "pdf_archive",
            "pdf_current",
            "pdf_raw",
            "pdf_temp",
        ]
        self.paths = {}
        for path in paths:
            path_data = self.addPath(path)
            self.paths[path_data[0]] = path_data[1]
        
    def addPath(self, path_name):
        full_path = os.path.join(self.cwd, path_name)
        if not os.path.isdir(full_path):
            os.mkdir(full_path)
        return [path_name,full_path]