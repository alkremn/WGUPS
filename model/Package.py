class Package:
    def __init__(self, id, locationId, deadline, weight, note, status):
        self.id = id
        self.locationId = locationId
        self.deadline = deadline
        self.truckId = None
        self.weight = weight
        self.note = note
        self.status = status
        self.deliveryTime = None

    def __str__(self):
        return str("%d, %s, %s, %s, %s,%s" %(self.id, self.locationId, self.deadline, self.status, self.note, self.deliveryTime))