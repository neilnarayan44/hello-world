import json, core, logging

# Checks whether a patient database already exists, if not creates one and saves as a json file
try:
    json.load(open('database.json'))
except:
    database = {}
    json.dump(database, open('database.json', 'w'))

# Checks whether a GP database already exists, if not creates one and saves as a json file
try:
    json.load(open('gp_database.json'))
except:
    gp_database = {}
    json.dump(gp_database, open('gp_database.json', 'w'))

# Checks whether an appointment database already exists, if not creates one and saves as a json file
try:
    json.load(open('appointments.json'))
except:
    appointments = {"Approved": {}, "Requested": {}, "Cancelled": {}}
    json.dump(appointments, open('appointments.json', 'w'))

# Create and configure logger
logging.basicConfig(filename="newfile.log",
                    format='%(asctime)s %(message)s',
                    filemode='a')

# Creating an object
logger = logging.getLogger()

# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)

# Test messages
logger.debug("Harmless debug Message")

logger.warning("Its a Warning")
logger.error("Did you try to divide by zero")

# Runs main program to start app
core.start_program()
