from Controller import Controller
from model.Time import Time
from model.Truck import Truck
from datastractures.Queue import Queue


controller = Controller()

truck1 = controller.truck1
truck2 = controller.truck2
truck3 = controller.truck3

dist1 = truck1.deliver_all()
dist2 = truck2.deliver_all()
dist3 = truck3.deliver_all()
#dist = truck2.calculate_distance(Time(8,20))
#list_ds = truck2.calculate_delivery(dist)

print(dist1 + dist2 + dist3)
print()

# sec_distance = controller.calculate_distance(controller.second_list)

# packages = controller.find_adj_locations(controller.late_list)
# first_distance = controller.calculate_distance(packages)

# third_list = []
# for key in controller.hub_packages.keys():
#     third_list.append(controller.hub_packages[key])


# truck = Truck(1,Time(8,0), controller.second_list)

# truck2 = Truck(2,Time(9,10))

# current_time = Time(10,0)
# distance1 = truck.calculate_distance(current_time)
# distance2 = truck2.calculate_distance(current_time)
# print(distance1)
# print(distance2)

# third_distance = controller.calculate_distance(third_list)
# print(first_distance)
# print(sec_distance)
# print(third_distance)
# print(first_distance + sec_distance + third_distance)