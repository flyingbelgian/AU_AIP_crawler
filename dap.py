import source, parser, output


class DAP:
    def __init__(self, airport, paths):
        # Gets current publication cycle and DAP source listing for current cycle
        dap_source = source.DAP(paths.path_dict['html_temp'])

        # Getting DAP source listing for specific airport
        dap_data = parser.DAPdata(
            dap_source.html,
            paths.path_dict['listing_current'],
            dap_source.pub_date,
            airport,
            )

        # Downloading all the relevant pdfs as listed in the airport specific DAP source listing
        for entry in dap_data.entries:
            pdf = source.DAPfile(entry[1], paths.path_dict['pdf_archive_raw'])

        # Generating the combined pdf
        dap_pdf = output.PdfOut(
            dap_data.panda,
            paths.path_dict['pdf_archive_raw'],
            paths.path_dict['pdf_current'],
            'DAP',
            airport,
            dap_source.pub_date,
            )
