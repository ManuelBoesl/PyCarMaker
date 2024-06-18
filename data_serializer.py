import constants
import json
from pycarmaker import Quantity
from traffic_object_data import TrafficObjectData


class DataSerializer:
    def __init__(self):
        self.status_dic = {-1: "Preprocessing", -2: "Idle", -3: "Postprocessing", -4: "Model Check",
                           -5: "Driver Adaption", -6: "FATAL ERROR", -7: "Waiting for License",
                           -8: "Simulation paused", -10: "Starting application", -11: "Simulink Initialization"}

    def serialize_data(self, ego_vehicle_data: TrafficObjectData, traffic_object_data_list: list, timestamp: Quantity,
                       sim_status: Quantity):
        serialized_data = {}
        serialized_data[constants.TIMESTAMP] = str(timestamp.data)
        serialized_data[constants.SIM_STATUS] = (
            "Running" if sim_status.data >= 0 else self.status_dic.get(sim_status.data))

        serialized_data[constants.EGO_VEHICLE] = {
            constants.POS_X: ego_vehicle_data.pos_x.data,
            constants.POS_Y: ego_vehicle_data.pos_y.data,
            constants.POS_Z: ego_vehicle_data.pos_z.data,
            constants.ROLL: ego_vehicle_data.roll.data,
            constants.PITCH: ego_vehicle_data.pitch.data,
            constants.YAW: ego_vehicle_data.yaw.data,
            constants.ID: ego_vehicle_data.id,
            constants.STEER_ANGLE: ego_vehicle_data.steer_angle.data
        }

        serialized_data[constants.OTHER_TRAFFIC_DATA] = []

        for traffic_object_data in traffic_object_data_list:
            serialized_data[constants.OTHER_TRAFFIC_DATA].append({
                constants.POS_X: traffic_object_data.pos_x.data,
                constants.POS_Y: traffic_object_data.pos_y.data,
                constants.POS_Z: traffic_object_data.pos_z.data,
                constants.ROLL: traffic_object_data.roll.data,
                constants.PITCH: traffic_object_data.pitch.data,
                constants.YAW: traffic_object_data.yaw.data,
                constants.ID: traffic_object_data.id,
                constants.STEER_ANGLE: traffic_object_data.steer_angle.data
            })

        return serialized_data

    def serialize_data_as_json(self, ego_vehicle_data: TrafficObjectData, traffic_object_data_list: list, timestamp: Quantity,
                               sim_status: Quantity):
        return json.dumps(self.serialize_data(ego_vehicle_data, traffic_object_data_list, timestamp, sim_status), indent=4)

