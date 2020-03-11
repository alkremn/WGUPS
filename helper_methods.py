from model.Time import Time

#These are helper methods for main to show all the info. Main purpose is readability

#printing the main menu
def print_menu():
    print("Please, make a choice(1-3):")
    print("1 - Status of the package by ID")
    print("2 - Status of all packagaes by time")
    print("3 - Exit\n")

def showPackageStatus(controller):
    while True:
        print("Enter package ID:")
        try:
            packageId = int(input("From 1 to %d: "%(controller.getPackagesCount())))
            if package_status(controller, packageId):
                break
        except ValueError:
            print("Its not a number. Please, try again!")
            print("-------------------------===========")

def get_input_time():
    while True:
        user_input = input("Please input the time in (HH:MM) format, between 8:00 and 17:00: ")
        hourMin = user_input.strip().split(":")
        try:
            if len(hourMin) < 2:
                raise ValueError
            hour = int(hourMin[0])
            mins = int(hourMin[1])
            return Time(hour, mins)
        except ValueError:
            print("Invalid format, Please try again!")

def package_status(controller, packageId):
    try:
        package = controller.getPackageById(packageId)
        truckId = package.truckId
        address = controller.getPackageAddress(package.locationId)
        status = controller.getStatus(package.status)
        deliveryTime = package.deliveryTime
        if deliveryTime is None:
            deliveryTime = "Not yet delivered"
        print("Package id: %d,truck id: %s, address: %s, status: %s, delivery time: %s\n"%(package.id,truckId,address,status,deliveryTime))
        return True
    except IndexError:
        print("Invalid package ID, Please try again")
        return False

def showAllPackages(controller):
    packages = controller.getAllPackages()
    print("Requested info:")
    for package in packages:
        truckId = package.truckId
        address = controller.getPackageAddress(package.locationId)
        status = controller.getStatus(package.status)
        deliveryTime = package.deliveryTime
        if deliveryTime is None:
            deliveryTime = "Not yet delivered"
        print("Package id: %d, truck id: %s, address: %s, status: %s, delivery time: %s"%(package.id, truckId, address,status,deliveryTime))
    print("\n")
