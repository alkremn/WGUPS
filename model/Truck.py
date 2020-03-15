import math
from datastractures.Queue import Queue
from model.Status import Status
from model.Time import Time

# Truck class that has list of route packages.
class Truck:
    # Constructor
    def __init__(self, id, start_time, load):
        self.id = id
        self.start_time = start_time
        self.SPEED = 18
        self.load_size = 0
        self.distance = 0
        self.dist_to_hub = 0
        self.total_distance = 0
        self.current_distance = 0
        self.loadQueue = self.loadTruck(load)
        self.delivered = []
        self.status = Status.IN_HUB

    # This method loads the truck by pushing each package into the queue and adds the distance to that location to the total distance
    # Then it adds distance to the hub.
    # Time-complexity is O(n) where n is the number of the packages
    def loadTruck(self, load):
        loadQueue = Queue()
        for package in load[0]:
            package[0].status = Status.IN_TRANSIT
            loadQueue.enqueue(package)
            self.total_distance += package[1]
            self.load_size += 1
        
        self.dist_to_hub = load[1]
        self.total_distance += load[1]
        return loadQueue

    # This method calculates the distance by the time stamp passed as an argument.
    def calculateDistance(self, current_time):
        time_span = current_time - self.start_time
        total_mins = time_span.get_mins()
        return (total_mins / 60) * self.SPEED
    
    # Main method of the Truck class that calculates the delivery, modifies each package and adding it to the delivered list.
    # Time-complexity is O(n) where n is the number of the packages in the queue
    def calculateDelivery(self, current_time):
        distance = self.calculateDistance(current_time)
        if distance == 0:
            self.status = Status.IN_HUB
            return

        if distance >= self.total_distance:
            self.status = Status.IN_HUB
            self.is_back = True
            self.deliverAll()
            self.current_distance = self.total_distance
            return 
            
        while self.loadQueue.head:
            loc_dist = self.loadQueue.head.item[1]
            distance -= loc_dist
            if distance < 0:
                distance += loc_dist
                break
            package = self.loadQueue.dequeue()
            package[0].status = Status.DELIVERED
            self.current_distance += package[1]
            package[0].deliveryTime = self.calculateDeliveryTime(self.start_time, self.current_distance)
            self.delivered.append(package)
       
        self.current_distance += distance
        self.status = Status.IN_TRANSIT
    
    # This method calculates the delivery time by start time and the distance.
    def calculateDeliveryTime(self, start_time, distance):
        raw_time = distance / self.SPEED
        hours = int(raw_time)
        mins = (raw_time - hours) * 60
        duration = Time(hours, mins)
        return start_time + duration

    # This method calculates the time for a full route.
    def calculateRouteTime(self):
        raw_time = self.total_distance / 18
        hours = int(raw_time)
        mins = math.ceil((raw_time - hours) * 60)
        duration = Time(hours, mins)
        return self.start_time + duration

    # This method getting each package from the queue and appends it to the delivered list and calculates the distance
    # Time-compexity is O(n) where n is number of packages in the queue
    def deliverAll(self):
        while self.loadQueue.head:
            package = self.loadQueue.dequeue()
            package[0].status = Status.DELIVERED
            self.current_distance += package[1]
            package[0].deliveryTime = self.calculateDeliveryTime(self.start_time, self.current_distance)
            self.delivered.append(package)
        return self.current_distance
            
    # This method resets all lists back to original load.
    # Time-complexity is O(n)
    def reset(self):
        while len(self.delivered) > 0:
            package = self.delivered.pop()
            package[0].status = Status.IN_TRANSIT
            package[0].deliveryTime = None
            self.loadQueue.front(package)
        self.current_distance = 0
        self.status = Status.IN_HUB
        return True