import source_old
import parser
import output


class Update:
    def __init__(self, airport, airac, paths):
        source_html = self.getSource(airac, paths.path_dict['html_archive'])
        source_listing = self.getListing(
            self.file_type,
            source_html.html,
            paths.path_dict['file_list_current'],
            source_html.current_date,
            airport,
        )
        for entry in source_listing.entries:
            self.getFile(paths.path_dict['pdf_archive_raw'], entry[1])
        # Generating the combined pdf
        output.PdfOut(
            source_listing.panda,
            paths.path_dict['pdf_archive_raw'],
            paths.path_dict['pdf_current'],
            self.file_type,
            airport,
            source_html.current_date,
        )


class DAP(Update):
    file_type = "DAP"
    getSource = source_old.DAPhtml
    getListing = parser.DAPdata
    getFile = source_old.DAPfile


class ERSA(Update):
    file_type = "ERSA"
    getSource = source_old.ERSAhtml
    getListing = parser.ERSAdata
    getFile = source_old.ERSAfile
