from pycarmaker import CarMaker, Quantity
import constants
import os
import time

# Read the environment variable IPGHOME
ipg_home_path = os.environ['IPGHOME']

rel_cm_exe_path = "carmaker/win64-11.0/bin/CM.exe"

cm = CarMaker(constants.CARMAKER_IP, constants.CARMAKER_PORT)

# 4 - Connect to CarMaker
cm.connect()

# 5 - Subscribe to vehicle speed
# Create a Quantity instance for vehicle speed (vehicle speed is a float type variable)
vehspd = Quantity("Car.v", Quantity.FLOAT)

# Initialize with negative speed to indicate that value was not read
vehspd.data = -1.0

# Subscribe (TCP socket need to be connected)
cm.subscribe(vehspd)

# Let's also read the simulation status (simulation status is not a quantity but a command
# so the command parameter must be set to True)
sim_status = Quantity("SimStatus", Quantity.INT, True)
cm.subscribe(sim_status)

# 6 - Read all subscribed quantities. In this example, vehicle speed and simulation status
# For some reason, the first two reads will be incomplete and must be ignored
# You will see 2 log errors like this: [ ERROR]   CarMaker: Wrong read
cm.read()
cm.read()
time.sleep(0.1)
c = 5
while(c > 0):
    c = c - 1
    # Read data from carmaker
    cm.read()
    print()
    print("Vehicle speed: " + str(vehspd.data * 3.6) + " km/h")
    print("Simulation status: " + ("Running" if sim_status.data >=
                                   0 else cm.status_dic.get(sim_status.data)))
    time.sleep(1)
