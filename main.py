import environment
import update

# Read list of aerodromes to be processed
with open("aerodromes.csv", 'r') as file:
    airports = file.read().splitlines()

# Set up all required folders
paths = environment.Paths()

# Move previously generated summary files to archive folders
paths.archiveFiles(paths.path_dict['listing_current'], paths.path_dict['listing_archive'])
paths.archiveFiles(paths.path_dict['pdf_current'], paths.path_dict['pdf_archive'])


for airport in airports:
    # Get current DAP files for each of the aerodromes
    dap_new = update.DAP(airport, paths)
    # Get current ERSA files for each of the aerodromes
    ersa_new = update.ERSA(airport, paths)
    # Get file listing for previous cycle
    print(paths.getLatestFile('DAP', airport, paths.path_dict['listing_archive']))
    print(paths.getLatestFile('ERSA', airport, paths.path_dict['listing_archive']))
    print(paths.getLatestFile('DAP', airport, paths.path_dict['listing_current']))
    print(paths.getLatestFile('ERSA', airport, paths.path_dict['listing_current']))
