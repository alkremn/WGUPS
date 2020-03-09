from datastractures.Hash_table import CustomHashTable

class Graph:
    def __init__(self):
        self.adjacent_locations = CustomHashTable()
        self.distances = CustomHashTable()
    
    def add_locations(self, locations):
        for key in locations.keys():
            loc_id = locations[key].id
            self.adjacent_locations[loc_id] = []
        return True

    def add_directed_distance(self, from_loc, to_loc, distance=1.0):
        self.distances[(from_loc.id, to_loc.id)] = distance
        self.adjacent_locations[from_loc.id].append(to_loc)

    def add_undirected_distance(self, loc_a, loc_b, distance=1.0):
        self.add_directed_distance(loc_a, loc_b, distance)
        self.add_directed_distance(loc_b, loc_a, distance)