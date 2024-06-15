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
vhcl_pos_x = Quantity("Vhcl.Fr1.x", Quantity.FLOAT)
vhcl_pos_y = Quantity("Vhcl.Fr1.y", Quantity.FLOAT)
vhcl_pos_z = Quantity("Vhcl.Fr1.z", Quantity.FLOAT)

pedestrian_x = Quantity("Traffic.T01.tx", Quantity.FLOAT)
pedestrian_y = Quantity("Traffic.T01.ty", Quantity.FLOAT)
pedestrian_z = Quantity("Traffic.T01.tz", Quantity.FLOAT)

cm.subscribe(vhcl_pos_x)
cm.subscribe(vhcl_pos_y)
cm.subscribe(vhcl_pos_z)

cm.subscribe(pedestrian_x)
cm.subscribe(pedestrian_y)
cm.subscribe(pedestrian_z)

cm.subscribe(sim_status)

# 6 - Read all subscribed quantities. In this example, vehicle speed and simulation status
# For some reason, the first two reads will be incomplete and must be ignored
# You will see 2 log errors like this: [ ERROR]   CarMaker: Wrong read
cm.read()
cm.read()
time.sleep(0.1)
c = 5

print("Waiting for CarMaker to start the sim")
cm.read()
while cm.status_dic.get(sim_status.data) != "Preprocessing":
    cm.read()
    print(cm.status_dic.get(sim_status.data))
    time.sleep(0.1)

print("Sim Started")

while(cm.status_dic.get(sim_status.data) != "Idle"):
    c = c - 1
    # Read data from carmaker
    cm.read()
    print()
    print("Vehicle speed: " + str(vehspd.data * 3.6) + " km/h")
    print("Simulation status: " + ("Running" if sim_status.data >=
                                   0 else cm.status_dic.get(sim_status.data)))
    
    print(f"Vhcl x: {vhcl_pos_x.data}")
    print(f"Vhcl y: {vhcl_pos_y.data}")
    print(f"Vhcl z: {vhcl_pos_z.data}")

    print(f"Ped x: {pedestrian_x.data}")
    print(f"Ped y: {pedestrian_y.data}")
    print(f"Ped z: {pedestrian_z.data}")

    time.sleep(1)
