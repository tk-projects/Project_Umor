class sensor_cluster:
    def __init__(self, cluster_id, groups, name='', location = None, owner = ''):
        self.cluster_id = cluster_id;
        self.groups = groups;
        self.name = name;
        self.location = location;
        self.owner = owner;