import source, parser, output


class ERSA:
    def __init__(self, airport, paths):
        # Gets current publication cycle and ERSA source listing for current cycle
        type = "ERSA"
        ersa_source = source.ERSAhtml(paths.path_dict['html_temp'])


        # Getting ERSA source listing for specific airport
        ersa_data = parser.ERSAdata(
            type,
            ersa_source.html,
            paths.path_dict['listing_current'],
            ersa_source.pub_date,
            airport,
            )

        # Downloading all the relevant pdfs as listed in the airport specific ERSA source listing
        for entry in ersa_data.entries:
            pdf = source.ERSAfile(paths.path_dict['pdf_archive_raw'],entry[1])

        # Generating the combined pdf
        ersa_pdf = output.PdfOut(
            ersa_data.panda,
            paths.path_dict['pdf_archive_raw'],
            paths.path_dict['pdf_current'],
            type,
            airport,
            ersa_source.pub_date,
            )
