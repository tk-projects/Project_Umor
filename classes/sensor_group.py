class sensor_group:
    def __init__(self, group_id, sensors, name='', location = None, owner = ''):
        self.group_id = group_id;
        self.name = name;
        self.location = location;
        self.owner = owner;
        self.sensors = sensors;

    def to_dict(self):
            return {
                "group_id": self.group_id,
                "name": self.name,
                "location": self.location,
                "unit": self.unit,
                "owner": self.owner,
                "sensors": self.sensors
            }