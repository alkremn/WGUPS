class Location:

    def __init__(self, id, address):
        self.id = id
        self.address = address
        self.distance = 0
        self.packages = []
        self.visited = False
        self.prev_location = None

    def __str__(self):
        return self.address + " visited: " + str(self.visited)
