import dap, environment, ersa

# Read list of aerodromes to be processed
with open("aerodromes.csv", 'r') as file:
    airports = file.read().splitlines()

# Set up all required folders
paths = environment.Paths()

# Get current DAP files for each of the aerodromes
_dap = []
for airport in airports:
    _dap.append(dap.DAP(airport, paths))

_ersa = []
for airport in airports:
    _ersa.append(ersa.ERSA(airport, paths))

# Cleaning up temporary folders that were used in other processes
paths.finalCleanUp()
