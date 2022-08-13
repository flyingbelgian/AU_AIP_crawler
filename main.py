import compare_notify
import csv
import environment
import update


# Set up all required folders and file paths
print("Setting up folder and file paths")
paths = environment.Paths()

# Read list of aerodromes to be processed
print("Reading aerodrome names")
with open(paths.aerodromes, 'r') as file:
    airports = file.read().splitlines()
# Read list of airac dates and cycles
print("Reading AIRAC cycle dates")
with open(paths.airac, 'r') as file:
    airac_source = csv.reader(file)
    next(airac_source)
    airac = [line for line in airac_source]
# Read list of subscriber emails
print("Reading subscriber emails")
with open(paths.subscribers, 'r') as file:
    subscribers = file.read().splitlines()

# Move previously generated summary files to archive folders
print("Moving last cycle's files to archive folders")
paths.archiveFiles(paths.path_dict['listing_current'], paths.path_dict['listing_archive'])
paths.archiveFiles(paths.path_dict['pdf_current'], paths.path_dict['pdf_archive'])

for airport in airports:
    # Get current DAP files for each of the aerodromes
    print(f"Getting latest DAP files for {airport}")
    dap_new = update.DAP(airport, airac, paths)
    # Get current ERSA files for each of the aerodromes
    print(f"Getting latest ERSA files for {airport}")
    ersa_new = update.ERSA(airport, airac, paths)
    # Get file listing for previous cycle
    print(f"Reading previous file listings for {airport}")
    csv_dap_previous = paths.getLatestFile('DAP', airport, paths.path_dict['listing_archive'])
    csv_ersa_previous = paths.getLatestFile('ERSA', airport, paths.path_dict['listing_archive'])
    # Get file listing for current cycle
    print(f"Reading current file listings for {airport}")
    csv_dap_current = paths.getLatestFile('DAP', airport, paths.path_dict['listing_current'])
    csv_ersa_current = paths.getLatestFile('ERSA', airport, paths.path_dict['listing_current'])

    # Runs comparison of link data and filenames of previously downloaded files against new files
    print(f"Comparing file listings for {airport}")
    compare_dap = compare_notify.Comparison(
        'DAP',
        airport,
        csv_dap_previous,
        csv_dap_current,
        paths.path_dict['report_archive'],
        subscribers)
    # # Runs comparison of content of previously downloaded files against new files
    # compare_ersa = compare_notify.Comparison('ERSA', airport, csv_ersa_previous, csv_ersa_current)
