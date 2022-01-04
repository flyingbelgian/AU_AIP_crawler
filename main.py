import environment, os, output, parser, source, time

# This to be replaced when creating functionality to iterate over list of airports to be processed
airport = "YAUR"

### FOR TESTING ONLY ##############################################################################
# import os
# dap_data = parser.DAPdata("html_archive/20211202_DAP_169.html", "20211202", airport)
# dap_pdf = output.PdfOut(dap_data.panda, 'pdf_source', 'DAP', airport, '20211202')
# def cleanUp():
#     cwd = os.getcwd()
#     for file_name in os.listdir(cwd):
#         if file_name.endswith('.html'):
#             os.replace(os.path.join(cwd, file_name), os.path.join(cwd, "html_archive", file_name))
# cleanUp()
###################################################################################################

### CODE BELOW TO BE COMMENTED OUT FOR TESTING ####################################################
# Set up all required folders
dir = environment.Paths()

# Getting DAP source
dap_source = source.DAP(dir.paths['html_temp'])

# Getting download data for current DAP
dap_data = parser.DAPdata(dap_source.html, dir.paths['listing_current'], dap_source.pub_date, airport)

# Downloading all the relevant pdfs
for entry in dap_data.entries:
    pdf = source.DAPfile(entry[1], dir.paths['pdf_temp'])

# Generating the combined pdf
dap_pdf = output.PdfOut(dap_data.panda, dir.paths['pdf_temp'], dir.paths['pdf_current'], 'DAP', airport, dap_source.pub_date)
   
# Cleaning up temporary source files that were used in other processes
def cleanUp(temp_path,archive_path):
    for file_name in os.listdir(temp_path):
        os.replace(os.path.join(temp_path, file_name), os.path.join(archive_path, file_name))
    os.rmdir(temp_path)
cleanUp(dir.paths['html_temp'], dir.paths['html_archive'])
# time.sleep(10)
cleanUp(dir.paths['pdf_temp'], dir.paths['pdf_raw'])