from Controller import Controller
from model.Time import Time
from model.Truck import Truck
from datastractures.Queue import Queue
import helper_methods as helper


print("\nWelcome to WGUPS package tracker!\n")
print("Hold on while we are calculating the route...\n")

controller = Controller()
total_distance = 0
for truck in controller.getTrucks():
    total_distance += truck.total_distance

print("We are using: %d trucks, with total miles: %.1f"%(controller.truckCount(), total_distance))
print("---------------------")

while True:
    helper.print_menu()
    try:
        user_input = int(input("Your choice: "))
        if user_input == 1:
            time = helper.get_input_time()
            controller.calculateDelivery(time)
            helper.showPackageStatus(controller)
        elif user_input == 2:
            time = helper.get_input_time()
            controller.calculateDelivery(time)
            helper.showAllPackages(controller)
        elif user_input == 3:
            exit()
        else:
            print("Invalid input! Try again!")
            print("-------------------------")

    except ValueError:
        print("Its not a number. Please, try again!")
        print("-------------------------===========")
    





