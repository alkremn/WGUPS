class Location:

    def __init__(self, id, address):
        self.id = id
        self.address = address
        self.packages = []

    def __str__(self):
        return self.address + " visited: " + str(self.visited)
