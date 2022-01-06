import dap
import environment
import ersa

# Read list of aerodromes to be processed
with open("aerodromes.csv", 'r') as file:
    airports = file.read().splitlines()

# Set up all required folders
paths = environment.Paths()

# Move previously generated summary files to archive folders
paths.archiveFiles(paths.path_dict['listing_current'], paths.path_dict['listing_archive'])
paths.archiveFiles(paths.path_dict['pdf_current'], paths.path_dict['pdf_archive'])

# Get current DAP files for each of the aerodromes
_dap = []
for airport in airports:
    _dap.append(dap.DAP(airport, paths))

# Get current ERSA files for each of the aerodromes
_ersa = []
for airport in airports:
    _ersa.append(ersa.ERSA(airport, paths))

# Compare file listings between previous cycle and current cycle


def ComparePublications():
    pass
