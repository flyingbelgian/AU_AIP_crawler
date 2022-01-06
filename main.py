import dap, environment

# Read list of aerodromes to be processed
with open("aerodromes.csv", 'r') as file:
    airports = file.read().splitlines()

# Set up all required folders
paths = environment.Paths()

# Get current DAP files for each of the aerodromes
daps = []
for airport in airports:
    daps.append(dap.DAP(airport, paths))

# Cleaning up temporary folders that were used in other processes
paths.finalCleanUp()
