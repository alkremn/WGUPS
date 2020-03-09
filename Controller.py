from model.Package import Package
from model.Location import Location
from datastractures.Hash_table import CustomHashTable
from datastractures.Graph import Graph
from datastractures.Queue import Queue
from model.Truck import Truck
from model.Time import Time
from model.Status import Status
class Controller:

    def create_locations(self):
        locations = CustomHashTable()
        addresses = self.get_addresses()
        for i in range(len(addresses)):
            locations[i] = Location(i, addresses[i])
        return locations


    def create_packages(self, locations):
        raw_package_values = self.read_csv_values("files/package_file.csv")
        package_list = self.split_str_values(raw_package_values)
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

# Creates graph with locations and distances between them
    def create_map(self, locations):
        location_map = Graph()
        location_map.add_locations(locations)
        distances = self.get_distances(locations)
        
        for dist in distances:
            fromLocation = locations[dist[0]]
            toLocation = locations[dist[1]]
            location_map.add_undirected_distance(fromLocation,toLocation,dist[2])
        
        return location_map

    def create_late_list(self, packagesIds):
        late_list = []
        for packId in packagesIds:
            package = self.hub_packages[packId]
            if package.note.startswith("Delayed"):
                late_list.append(packId)
                self.avb_packs.pop(self.avb_packs.index(packId))
        return late_list

    def create_wrong_add_list(self, packagesIds):
        wrong_address_list = []
        for packId in packagesIds:
            package = self.hub_packages[packId]
            if package.note.startswith("Wrong address"):
                wrong_address_list.append(packId)
                
        for packId in wrong_address_list:
            self.avb_packs.pop(self.avb_packs.index(packId))
        return wrong_address_list

    def create_second_list(self, packagesIds):
        sec_list = set()
        for packId in packagesIds:
            package = self.hub_packages[packId]
            if package.note.startswith("Can only be on truck 2"):
                sec_list.add(packId)
            elif package.note.startswith("Must"):
                sec_list.add(packId)
                package_ids = self.process_notes(package.note)
                for packageId in package_ids:
                    sec_list.add(packageId)
        
        for packId in sec_list:
            self.avb_packs.pop(self.avb_packs.index(packId))

        sec_list = self.find_packages(sec_list)
        sec_list = self.sort_packages(sec_list)
        sec_list = self.find_adj_locations(sec_list[0])
        return self.sort_packages(sec_list)


    def create_first_list(self, late_list, wrong_add_list, avb_packs):
        first_list = []
        first_list.extend(late_list)
        first_list.extend(wrong_add_list)
        first_list = self.find_packages(first_list)
        first_list = self.sort_packages(first_list)
        first_list = self.find_adj_locations(first_list[0])
        first_list = self.sort_packages(first_list)

        return first_list

    def create_third_list(self, avb_packs):
        third_list = [pack for pack in avb_packs]
        avb_packs.clear()
        third_list = self.sort_packages(third_list)
        return third_list

    def find_packages(self, packageIds):
        all_packages = set()
        for packageId in packageIds:
            all_packages.add(packageId)
            package = self.hub_packages[packageId]
            location = self.locations[package.locationId]
            for packId in location.packages:
                all_packages.add(packId)
                if packId in self.avb_packs:
                    self.avb_packs.pop(self.avb_packs.index(packId))
        return all_packages


    def find_adj_locations(self, packageIds):
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
                main_distance = self.get_distance(package_one.locationId, package_two.locationId)
                for key in self.avb_packs:
                    package = self.hub_packages[key]
                    first_distance = self.get_distance(package_one.locationId, package.locationId)
                    sec_distance = self.get_distance(package_two.locationId, package.locationId)
                    if first_distance < main_distance and sec_distance < main_distance:
                        #%s" %(main_distance,address_one,first_distance, address_bet, sec_distance, address_two, ))
                        add_packages.add(package.id)
                       
        for packId in add_packages:
            if len(ids) >= 16:
                break
            self.avb_packs.pop(self.avb_packs.index(packId))
            ids.add(packId)
            
        return list(ids)



    # def calculate_distance(self, packages):
    #     packages = self.sort_packages(packages)
    #     start = self.locations[0]
    #     total_distance = self.get_distance(start.id, packages[0].locationId)
    #     print("%s to %s is %.1f"% (start.address, self.locations[packages[0].locationId].address, total_distance))

    #     for i in range(1, len(packages)):
    #         from_loc_id = packages[i-1].locationId
    #         to_loc_id = packages[i].locationId
    #         distance = self.get_distance(from_loc_id, to_loc_id)
    #         total_distance += distance
    #         print("%s to %s is %.1f"% (self.locations[from_loc_id].address, self.locations[to_loc_id].address, distance))
    #         print(total_distance)

    #     last_loc_id = packages[len(packages)-1].locationId
    #     distance = self.get_distance(last_loc_id, start.id)
    #     total_distance += distance
    #     print("%s to %s is %.1f"% (self.locations[last_loc_id], start.address, distance))
    #     print(total_distance)
        
    #     return total_distance

    def sort_packages(self, packagesIds):
        packagesIds = list(packagesIds)
        sorted_list = []
        currentLocId = self.locations[0].id
        while len(packagesIds) > 0:
            index = 0
            smallest_distance = float("inf")
            for i in range(len(packagesIds)):
                package = self.hub_packages[packagesIds[i]]
                location = self.locations[package.locationId]
                distance = self.get_distance(currentLocId, location.id)
                if distance < smallest_distance:
                    smallest_distance = distance
                    index = i
            packageId = packagesIds.pop(index)
            currentLocId = self.locations[self.hub_packages[packageId].locationId].id
            sorted_list.append((packageId, smallest_distance))
        lastId = sorted_list[len(sorted_list)-1][0]
        package = self.hub_packages[lastId]
        location = self.locations[package.locationId]
        last_dist = self.get_distance(location.id, 0)
        #sorted_list.append((0,last_dist))
        return (sorted_list, last_dist)

    def __init__(self):
        self.locations = self.create_locations()
        self.location_map = self.create_map(self.locations)
        self.hub_packages = self.create_packages(self.locations)
        self.avb_packs = self.hub_packages.keys()[:]
        self.late_list = self.create_late_list(self.avb_packs)
        self.wrong_add_list = self.create_wrong_add_list(self.avb_packs)
        self.second_list = self.create_second_list(self.avb_packs)
        self.first_list = self.create_first_list(self.late_list, self.wrong_add_list, self.avb_packs)
        self.third_list = self.create_third_list(self.avb_packs)
        self.truck2 = Truck(2, Time(8,0), self.second_list)
        self.truck1 = Truck(1,Time(9,5), self.first_list)
    #helper methods that read values from the files
    
    #Reads in all address values from the file


    def get_distance(self, from_loc_id, to_loc_id):
        return self.location_map.distances[from_loc_id, to_loc_id]

    def process_notes(self, note):
        words = note.split(" ")
        numbers = []
        for word in words:
            if str.isdigit(word):
                numbers.append(int(word))
        return numbers

    def get_distances(self, locations):
        distances = self.read_csv_values("files/distance.csv")
        distances = self.split_str_values(distances)
        distance_list = []
        
        for j in range(len(locations.keys())):
            for i in range(j, len(locations.keys())):
                distance_list.append((locations[j].id, locations[i].id, float(distances[i][j])))
        return distance_list

    def get_addresses(self):
        addresses_strings = self.read_csv_values("files/addresses.csv")
        addresses = self.strip_str_values(addresses_strings)
        return addresses

    def read_csv_values(self, file_name):
        values_list = []
        f = open(file_name, "r")
        line = f.readline()
        while line:
            values_list.append(line)
            line = f.readline()
        f.close()
        return values_list

    def split_str_values(self, raw_values):
        values_list = []
        for value_str in raw_values:
            value_str = value_str.strip("\n")
            values_list.append(value_str.split(","))
        return values_list

    def strip_str_values(self, values):
        values_list = []
        for value in values:
            values_list.append(value.strip("\n"))
        return values_list