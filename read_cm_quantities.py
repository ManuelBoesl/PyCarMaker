from pycarmaker import CarMaker, Quantity
import constants
import time
from traffic_object_data import TrafficObjectData
import json
import os
from data_serializer import DataSerializer
from udp_sender import UdpSender

class ReadCMQuantities:
    def __init__(self):
        self.cm = CarMaker(constants.CARMAKER_IP, constants.CARMAKER_PORT)
        self.cm.connect()

        self.ego_vehicle_data = TrafficObjectData(self.cm)
        self.traffic_object_data_list = []
        self.sim_status = Quantity("SimStatus", Quantity.INT, True)
        self.timestamp = Quantity("Time", Quantity.FLOAT)
        self.traffic_object_ids = []

        self.data_serializer = DataSerializer()
        self.udp_sender = UdpSender()

        self.read_traffic_object_dict()
        self.subscribe_to_quantities()
        self.wait_for_start()
        self.read_cm_quantities()

    def read_traffic_object_dict(self):
        # get the path to the directory of this file
        current_dir = os.path.dirname(os.path.realpath(__file__))
        # get the path to the traffic object config file
        traffic_object_config_path = os.path.join(current_dir, "traffic_configuration.json")
        traffic_object_config_dict = None
        with open(traffic_object_config_path, "r") as f:
            traffic_object_config_dict = json.load(f)

        self.traffic_object_ids = traffic_object_config_dict[constants.TRAFFIC_IDS]

    def subscribe_to_quantities(self):
        self.cm.subscribe(self.timestamp)
        self.cm.subscribe(self.sim_status)

        self.ego_vehicle_data.pos_x = Quantity("Vhcl.Fr1.x", Quantity.FLOAT)
        self.ego_vehicle_data.pos_y = Quantity("Vhcl.Fr1.y", Quantity.FLOAT)
        self.ego_vehicle_data.pos_z = Quantity("Vhcl.Fr1.z", Quantity.FLOAT)
        self.ego_vehicle_data.roll = Quantity("Vhcl.Roll", Quantity.FLOAT)
        self.ego_vehicle_data.pitch = Quantity("Vhcl.Pitch", Quantity.FLOAT)
        self.ego_vehicle_data.yaw = Quantity("Vhcl.Yaw", Quantity.FLOAT)
        self.ego_vehicle_data.id = "EgoVehicle"
        self.ego_vehicle_data.steer_angle = Quantity("Vhcl.Steer.Ang", Quantity.FLOAT)
        self.ego_vehicle_data.subscribe()

        for traffic_object_id in self.traffic_object_ids:
            current_traffic_object = TrafficObjectData(self.cm)
            current_traffic_object.id = traffic_object_id
            current_traffic_object.pos_x = Quantity("Traffic." + traffic_object_id + ".tx", Quantity.FLOAT)
            current_traffic_object.pos_y = Quantity("Traffic." + traffic_object_id + ".ty", Quantity.FLOAT)
            current_traffic_object.pos_z = Quantity("Traffic." + traffic_object_id + ".tz", Quantity.FLOAT)
            current_traffic_object.roll = Quantity("Traffic." + traffic_object_id + ".rx", Quantity.FLOAT)
            current_traffic_object.pitch = Quantity("Traffic." + traffic_object_id + ".ry", Quantity.FLOAT)
            current_traffic_object.yaw = Quantity("Traffic." + traffic_object_id + ".rz", Quantity.FLOAT)
            current_traffic_object.steer_angle = Quantity("Traffic." + traffic_object_id + ".SteerAng", Quantity.FLOAT)
            current_traffic_object.subscribe()
            self.traffic_object_data_list.append(current_traffic_object)

    def wait_for_start(self):
        print("Waiting for CarMaker to start the sim")
        self.cm.read()
        while self.cm.status_dic.get(self.sim_status.data) != "Preprocessing":
            self.cm.read()
            print(self.cm.status_dic.get(self.sim_status.data))
            time.sleep(0.001)

        print("CarMaker started the sim")

    def read_cm_quantities(self):
        self.cm.read()

        while self.sim_status.data >= 0 or self.cm.status_dic.get(self.sim_status.data) == "Preprocessing":
            self.cm.read()
            serialized_json_data = self.data_serializer.serialize_data_as_json(self.ego_vehicle_data, self.traffic_object_data_list, self.timestamp, self.sim_status)
            # self.udp_sender.send_json(serialized_json_data)
            if self.sim_status.data >= 0:
                self.udp_sender.write_to_file(serialized_json_data)
            time.sleep(0.001)

if __name__ == '__main__':
    ReadCMQuantities()

