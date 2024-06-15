from pycarmaker import CarMaker
class TrafficObjectData:
    def __init__(self, cm_instance: CarMaker):
        self.cm_instance = cm_instance
        self.pos_x = None
        self.pos_y = None
        self.pos_z = None
        self.roll = None
        self.pitch = None
        self.yaw = None
        self.id = None
        self.steer_angle = None

    def subscribe(self):
        self.cm_instance.subscribe(self.pos_x)
        self.cm_instance.subscribe(self.pos_y)
        self.cm_instance.subscribe(self.pos_z)
        self.cm_instance.subscribe(self.roll)
        self.cm_instance.subscribe(self.pitch)
        self.cm_instance.subscribe(self.yaw)
        self.cm_instance.subscribe(self.steer_angle)

