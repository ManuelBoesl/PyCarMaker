import socket
import constants
import os


class UdpSender:
    def __init__(self):
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.package_counter = 0
        # self.udp_socket.bind((constants.UNITY_IP, constants.UNITY_PORT))

    def send_json(self, json_data):
        self.udp_socket.sendto(json_data.encode(), (constants.UNITY_IP, constants.UNITY_PORT))

    def write_to_file(self, json_data):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        test_json_files_dir = os.path.join(current_dir, "test_json_files")
        current_file_name = "test_json_" + str(self.package_counter) + ".json"
        current_file_path = os.path.join(test_json_files_dir, current_file_name)
        with open(current_file_path, "w") as f:
            f.write(json_data)
        self.package_counter += 1
