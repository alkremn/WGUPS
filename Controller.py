from model.Package import Package
from model.Location import Location
from datastractures.Hash_table import CustomHashTable
from datastractures.Graph import Graph
from model.Truck import Truck
from model.Time import Time
from model.Status import Status

# This is a main class Controller that reads all data in, initializes fields. 
class Controller:

    # This method creates Location objects 
    # time-complexity O(n)
    def createLocations(self):
        locations = CustomHashTable()
        addresses = self.getAddresses()
        for i in range(len(addresses)):
            locations[i] = Location(i, addresses[i])
        return locations

    # This method creats Package objects 
    # Time-complexity is O(n^2) since we have a second "for" loop to go through all locations and find 
    # the location that the package is for.
    # Then we add this package to the location list. 
    def createPackages(self, locations):
        raw_package_values = self.readCSVValues("files/package_file.csv")
        package_list = self.splitStrValues(raw_package_values)
        packages = CustomHashTable()
        for package_str in package_list:
            address = package_str[1] + " " + package_str[4]
            for key in locations.keys():
                location = locations[key]
                sec_address = location.address
                if address == sec_address:
                    locationId = key
                    package = Package(int(package_str[0]),locationId, package_str[5],package_str[6],package_str[7],Status.IN_HUB) 
                    packages[package.id] = package
                    if package not in location.packages:
                        location.packages.append(package.id)
        return packages

    # Creates graph with locations and distances between them. Using "for" loop to go through all distances.
    # Time-complexity is O(n) 
    def createMap(self, locations):
        location_map = Graph()
        location_map.add_locations(locations)
        distances = self.readDistances(locations)
        
        for dist in distances:
            fromLocation = locations[dist[0]]
            toLocation = locations[dist[1]]
            location_map.add_undirected_distance(fromLocation,toLocation,dist[2])
        
        return location_map

    # Creates late list by sorting the available packages list
    # Time-complexity is O(n)
    def createLateList(self, packagesIds):
        late_list = []
        for packId in packagesIds:
            package = self.hub_packages[packId]
            if package.note.startswith("Delayed"):
                late_list.append(packId)
                self.avb_packs.pop(self.avb_packs.index(packId))
        return late_list

    # Finds the package with the wrong address listed, using 2 loops.
    # Time-complexity is O(n + n) = O(n)
    def createWrongList(self, packagesIds):
        wrongAddressList = []
        for packId in packagesIds:
            package = self.hub_packages[packId]
            if package.note.startswith("Wrong address"):
                wrongAddressList.append(packId)
                
        for packId in wrongAddressList:
            self.avb_packs.pop(self.avb_packs.index(packId))
        return wrongAddressList

    # Finds eary delivery packages and adds them to the list.
    # Time-complexity is O(n+n) = O(n)
    def getEarlyDevList(self, avb_packs):
        earlyDevList = []
        for packageId in avb_packs:
            package = self.hub_packages[packageId]
            if package.deadline.startswith("10:30"):
                earlyDevList.append(packageId)

        for packageId in earlyDevList:
            self.avb_packs.pop(self.avb_packs.index(packageId))
        
        return earlyDevList

    # Creates list of the packages for the second truck.
    # Time-complexity is O(n^2) because of the second "for" loop
    def createSecondList(self, packagesIds):
        sec_list = set()
        for packageId in packagesIds:
            package = self.hub_packages[packageId]
            if package.note.startswith("Can only be on truck 2"):
                sec_list.add(packageId)
            elif package.note.startswith("Must"):
                sec_list.add(packageId)
                package_ids = self.processNotes(package.note)
                for packageId in package_ids:
                    sec_list.add(packageId)
                
        for packageId in sec_list:
            self.avb_packs.pop(self.avb_packs.index(packageId))

        while len(sec_list) < 16 and len(self.early_dev_list) > 0:
            sec_list.add(self.early_dev_list.pop())

        sec_list = self.findPackages(sec_list)
        sec_list = self.sortPackages(sec_list)
        sec_list = self.findNearLocations(sec_list[0])
        return self.sortPackages(sec_list)

    
    # Creates list of the packages for the first truck.
    # Time-complexity is O(n).
    def createFirstList(self, late_list, early_dev_list, avb_packs):
        first_list = []
        first_list.extend(late_list)
        late_list.clear()
        first_list.extend(early_dev_list)
        first_list = self.findPackages(first_list)
        first_list = self.sortPackages(first_list)
        first_list = self.findNearLocations(first_list[0])
        first_list = self.sortPackages(first_list)
        return first_list

    # Creates list of the packages for the third truck.
    # Time-complexity is O(n).
    def createThirdList(self, avb_packs, wrong_add_list):
        third_list = [pack for pack in avb_packs]
        avb_packs.clear()
        third_list.extend(wrong_add_list)
        third_list = self.sortPackages(third_list)
        return third_list

    # Finds addition packages that might have the same destination as the package from the parameter list
    # Time-complexity is O(n^2) since we have second loop to go through the available packages.
    def findPackages(self, packageIds):
        all_packages = set(packageIds)
        for packageId in packageIds:
            all_packages.add(packageId)
            package = self.hub_packages[packageId]
            location = self.locations[package.locationId]
            for packId in location.packages:
                if packId in self.avb_packs:
                    if len(all_packages) >= 16:
                        return all_packages
                    all_packages.add(packId)
                    self.avb_packs.pop(self.avb_packs.index(packId))
        return all_packages

    #That is main algorithm that utilizes the greedy approach to find from 
    def findNearLocations(self, packageIds):
        add_packages = set()
        count = len(packageIds)
        ids = set()
        for id in packageIds:
            ids.add(id[0])

        for i in range(1, len(packageIds)):
            packId1 = packageIds[i-1][0]
            packId2 = packageIds[i][0]
            package_one = self.hub_packages[packId1]
            package_two = self.hub_packages[packId2]
            if package_one.locationId != package_two.locationId:
                main_distance = self.getDistance(package_one.locationId, package_two.locationId)
                for key in self.avb_packs:
                    package = self.hub_packages[key]
                    first_distance = self.getDistance(package_one.locationId, package.locationId)
                    sec_distance = self.getDistance(package_two.locationId, package.locationId)
                    if first_distance < main_distance and sec_distance < main_distance:
                        add_packages.add(package.id)
                       
        for packageId in add_packages:
            if len(ids) >= 16:
                break
            self.avb_packs.pop(self.avb_packs.index(packageId))
            ids.add(packageId)
            
        return list(ids)

    def sortPackages(self, packagesIds):
        packagesIds = list(packagesIds)
        sorted_list = []
        currentLocId = self.locations[0].id
        while len(packagesIds) > 0:
            index = 0
            smallest_distance = float("inf")
            for i in range(len(packagesIds)):
                package = self.hub_packages[packagesIds[i]]
                location = self.locations[package.locationId]
                distance = self.getDistance(currentLocId, location.id)
                if distance < smallest_distance:
                    smallest_distance = distance
                    index = i
            packageId = packagesIds.pop(index)
            currentLocId = self.locations[self.hub_packages[packageId].locationId].id
            sorted_list.append((packageId, smallest_distance))
        lastId = sorted_list[len(sorted_list)-1][0]
        package = self.hub_packages[lastId]
        location = self.locations[package.locationId]
        last_dist = self.getDistance(location.id, 0)
        return (sorted_list, last_dist)

    # This is an interface method that is called from main.py to calculate the data by spacific time stamp
    # that was passed as a parameter.
    # Time complexity is O(n) where n is number of the trucks
    def calculateDelivery(self, time):
        for truck in self.trucks:
            truck.reset()       
            truck.calculateDelivery(time)

        return self.getTrucks()

    # This is an interface method that returns the number of the trucks
    def getTrucks(self):
        return self.trucks

    # Constructor method that initializes all fields, calculates the routes.
    def __init__(self):
        self.locations = self.createLocations()
        self.location_map = self.createMap(self.locations)
        self.hub_packages = self.createPackages(self.locations)
        self.avb_packs = self.hub_packages.keys()[:]
        self.trucks = []
        self.late_list = self.createLateList(self.avb_packs)
        self.early_dev_list = self.getEarlyDevList(self.avb_packs)
        self.wrongList = self.createWrongList(self.avb_packs)
        self.second_list = self.createSecondList(self.avb_packs)
        self.first_list = self.createFirstList(self.late_list,self.early_dev_list, self.avb_packs)
        self.third_list = self.createThirdList(self.avb_packs, self.wrongList)
        self.trucks.append(Truck(2, Time(8,0), self.getPackagesByID(self.second_list, 2)))
        self.trucks.append(Truck(1,Time(9,5), self.getPackagesByID(self.first_list,1)))
        self.trucks.append(Truck(3, Time(10,20), self.getPackagesByID(self.third_list,3)))
    
    
    def truckCount(self):
        return len(self.trucks)

    def getPackagesByID(self, packageIds, truckId):
        packages = []
        for packId in packageIds[0]:
            package = self.hub_packages[packId[0]]
            package.truckId = truckId
            packages.append((package, packId[1]))
        return (packages, packageIds[1])

    # helper methods that read values from the files
    
    # Returns the address object by the locaion Id
    # Time-complexity is O(1) constant since it utilizes Hash table.
    def getPackageAddress(self, locationId):
        return self.locations[locationId].address

    # Modifies the status from Enumeration to readable string and returns it
    def getStatus(self, status):
        if status == Status.IN_HUB: return "In Hub"
        elif status ==Status.IN_TRANSIT: return "In transit"
        else: return "Delivered"

    # Method returns the package by package id.
    # Time-complexity is O(1) constant.
    def getPackageById(self, packageId):
        if packageId not in self.hub_packages.keys():
            raise IndexError
        return self.hub_packages[packageId]

    def getAllPackages(self):
        packages = []
        for packageId in self.hub_packages.keys():
            packages.append(self.hub_packages[packageId])
        return packages

    def getPackagesCount(self):
        return len(self.hub_packages.keys())

    def calculateTotalDist(self, route):
        total_dist = 0
        for pack in route[0]:
            total_dist += pack[1]
        return total_dist + route[1]
    
    def getDistance(self, from_loc_id, to_loc_id):
        return self.location_map.distances[from_loc_id, to_loc_id]

    def processNotes(self, note):
        words = note.split(" ")
        numbers = []
        for word in words:
            if str.isdigit(word):
                numbers.append(int(word))
        return numbers

    def readDistances(self, locations):
        distances = self.readCSVValues("files/distance.csv")
        distances = self.splitStrValues(distances)
        distance_list = []
        
        for j in range(len(locations.keys())):
            for i in range(j, len(locations.keys())):
                distance_list.append((locations[j].id, locations[i].id, float(distances[i][j])))
        return distance_list

    def getAddresses(self):
        addresses_strings = self.readCSVValues("files/addresses.csv")
        addresses = self.stripStrValues(addresses_strings)
        return addresses

    # Reads in all address values from the file
    # Time-complexity is O(n) where n is number of lines in the file
    def readCSVValues(self, file_name):
        values_list = []
        f = open(file_name, "r")
        line = f.readline()
        while line:
            values_list.append(line)
            line = f.readline()
        f.close()
        return values_list

    # Splits string by comma and returns a list
    # Time-complexity is O(n)
    def splitStrValues(self, raw_values):
        values_list = []
        for value_str in raw_values:
            value_str = value_str.strip("\n")
            values_list.append(value_str.split(","))
        return values_list

    # Removes "\n" in the string and returs a list
    # Time-complexity is O(n)
    def stripStrValues(self, values):
        values_list = []
        for value in values:
            values_list.append(value.strip("\n"))
        return values_list