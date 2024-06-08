class sensor_group:
    def __init__(self, group_id, sensors, name='', location = None, owner = ''):
        self.group_id = group_id;
        self.name = name;
        self.location = location;
        self.owner = owner;
        self.sensors = sensors;

    def to_dict(self):
            sensors_to_dict = {};
            for i in range(1,len(self.sensors)+1):
                sensors_to_dict[i] = self.sensors[i].sensor_id;
                print(self.sensors[i].name, "was converted into dict with its ID:",self.sensors[i].sensor_id)

            return {
                "group_id": self.group_id,
                "name": self.name,
                "location": self.location,
                "owner": self.owner,
                "sensors":sensors_to_dict
                
                
                    
            }