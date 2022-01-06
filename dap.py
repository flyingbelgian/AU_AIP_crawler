import source
import parser
import output


class DAP:
    def __init__(self, airport, paths):
        # Gets current publication cycle and DAP source listing for current cycle
        type = "DAP"
        dap_source = source.DAPhtml(paths.path_dict['html_archive'])

        # Getting DAP source listing for specific airport
        dap_data = parser.DAPdata(
            type,
            dap_source.html,
            paths.path_dict['listing_current'],
            dap_source.pub_date,
            airport,
        )

        # Downloading all the relevant pdfs as listed in the airport specific DAP source listing
        for entry in dap_data.entries:
            pdf = source.DAPfile(paths.path_dict['pdf_archive_raw'], entry[1])

        # Generating the combined pdf
        dap_pdf = output.PdfOut(
            dap_data.panda,
            paths.path_dict['pdf_archive_raw'],
            paths.path_dict['pdf_current'],
            type,
            airport,
            dap_source.pub_date,
        )
