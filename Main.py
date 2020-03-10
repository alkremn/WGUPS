from Controller import Controller
from model.Time import Time
from model.Truck import Truck
from datastractures.Queue import Queue

def print_menu():
    print("Please, make a choice:")
    print("1 - Status of the package by ID")
    print("2 - Status of all packagaes by Timestamp")
    print("3 - Exit")

def package_status(packageId):
    try:
        
        package = controller.get_package_by_id(packageId)
        print(package)
        return True
    
    except IndexError:
        print("Invalid package ID, Please try again")
        return False

def get_package_id():
    while True:
        print("Enter package ID:")
        try:
            user_input = int(input("From 1 to %d: "%(controller.get_packages_count())))
            if package_status(user_input):
                break

        except ValueError:
            print("Its not a number. Please, try again!")
            print("-------------------------===========")


print("Welcome to WGUPS package tracker!")
print("Hold on while we are calculating the route...")

controller = Controller()
total_distance = controller.truck1.total_distance + controller.truck2.total_distance + controller.truck3.total_distance

print("Total miles are: %.1f"%(total_distance))

controller.get_stat_by_time(Time(9,20))

while True:
    print_menu()
    try:
        user_input = int(input("Your choice: "))
        if user_input == 1:
            get_package_id()
        elif user_input == 2:
            print("your choice is 2")
        elif user_input == 3:
            exit()
        else:
            print("Invalid input! Try again!")
            print("-------------------------")

    except ValueError:
        print("Its not a number. Please, try again!")
        print("-------------------------===========")
    





















# tr1, tr2, tr3 = controller.get_stat_by_time(Time(12,50))

# print("1 truck")
# print(tr1.loadtoList())
# print(tr1.deliveredToList())
# print(tr1.current_distance)
# print(tr1.status)
# print(tr1.calculate_route_time())
# print("--------------")
# print("2 truck")
# print(tr2.loadtoList())
# print(tr2.deliveredToList())
# print(tr2.current_distance)
# print(tr2.status)
# print(tr2.calculate_route_time())
# print("--------------")
# print("3 truck")
# print(tr3.loadtoList())
# print(tr3.deliveredToList())
# print(tr3.current_distance)
# print(tr3.status)
# print(tr3.calculate_route_time())
# print("--------------")

# print(tr1.current_distance + tr2.current_distance + tr3.current_distance)