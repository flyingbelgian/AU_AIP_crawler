import output
import paths

# Set up all required folders and file paths
print("Setting up folder and file paths")
paths = paths.Paths()

# Read list of aerodromes to be processed
print("Reading aerodrome names")
with open(paths.aerodromes, 'r') as file:
    airports = file.read().splitlines()

import source

for airport in airports:
    ### Download all files and get file listings for all types and cycles found
    DAPfiles = source.getDAPfiles(airport)
    for cycle in DAPfiles:
        output.combinePDF(airport,"DAP",cycle)
    ERSAfiles = source.getERSAfiles(airport)
    for cycle in ERSAfiles:
        output.combinePDF(airport,"ERSA",cycle)
