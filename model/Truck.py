import math
from datastractures.Queue import Queue
from model.Status import Status
from model.Time import Time

class Truck:
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

    def calculateDistance(self, current_time):
        time_span = current_time - self.start_time
        total_mins = time_span.get_mins()
        return (total_mins / 60) * self.SPEED
    

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
    

    def calculateDeliveryTime(self, start_time, distance):
        raw_time = distance / self.SPEED
        hours = int(raw_time)
        mins = (raw_time - hours) * 60
        duration = Time(hours, mins)
        return start_time + duration


    def calculateRouteTime(self):
        raw_time = self.total_distance / 18
        hours = int(raw_time)
        mins = math.ceil((raw_time - hours) * 60)
        duration = Time(hours, mins)
        return self.start_time + duration


    def deliverAll(self):
        while self.loadQueue.head:
            package = self.loadQueue.dequeue()
            package[0].status = Status.DELIVERED
            self.current_distance += package[1]
            package[0].deliveryTime = self.calculateDeliveryTime(self.start_time, self.current_distance)
            self.delivered.append(package)
        return self.current_distance
            
    def loadtoList(self):
        packages = []
        current = self.loadQueue.head
        while current:
            packages.append(current.item[0])
            current = current.next
        return packages

    def deliveredToList(self):
        delivered_list = []
        for pack in self.delivered:
            delivered_list.append(pack[0])
        return delivered_list

    def reset(self):
        while len(self.delivered) > 0:
            package = self.delivered.pop()
            package[0].status = Status.IN_TRANSIT
            package[0].deliveryTime = None
            self.loadQueue.front(package)
        self.current_distance = 0
        self.status = Status.IN_HUB
        return True