class sensor_cluster:
    def __init__(self, groups, cluster_id, name='', location = None, owner = ''):
        self.cluster_id = cluster_id;
        self.groups = groups;
        self.name = name;
        self.location = location;
        self.owner = owner;