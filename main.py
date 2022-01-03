import parser, source

# Getting DAP source
# Comment out for testing to avoid loading AirServices website
dap_source = source.DAP()
dap_source.saveSource()

# # Uncomment for testing
# dap_data = parser.DAPdata("20211202_DAP_169.html", "20211202", "YSSY")
# dap_data.writeDAPcsv()

# Getting download data for current DAP
# Comment out for testing
dap_data = parser.DAPdata(dap_source.html, dap_source.pub_date, "YSBY")
dap_data.writeDAPcsv()

# Downloading all the relevant pdfs
# Comment out for testing
for entry in dap_data.entries:
    pdf = source.DAPfile(entry[1])