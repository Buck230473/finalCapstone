# import tabulate module
from tabulate import tabulate

#========The beginning of the class==========
class Shoe:
    # constructor
    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    # displays the product name and the cost of a user specified product
    def get_cost(self):
        print(f"\n{self.product} cost R{self.cost}")

    # displays the quantity of a user specified product
    def get_quantity(self):
        print(f"\nThere are currently {self.quantity} x {self.product} in stock")

    # returns a string representation of a class
    def __str__(self):
        return (f"\nCountry - {self.country}, SKU - {self.code}, Product - {self.product}, Cost - {self.cost}, Quantity - {self.quantity}")

# intialise shoes_objects list to store the Shoe objects
shoes_objects = []

# reads the data from inventory.txt and returns a list of objects
def read_shoes_data():
    # clears any data that might have been previously stored in shoes_objects
    shoes_objects = []
    # opens inventory.txt in read mode
    try:
        with open("inventory.txt", "r") as file:
            lines = file.readlines()

            # loops through the file and strips and splits
            for line in lines:
                temp = line.strip()
                temp = temp.split(",")

                # ignores the first line which is just the headings
                if temp[0] != "Country":
                    # adds the information to the shoes_objects list in the form of objects
                    try:
                        shoes_objects.append(Shoe(temp[0], temp[1], temp[2], temp[3], temp[4])) # creates the object but this is not relevant yet
                    except IndexError:
                        print("Error - could not read record")
        return(shoes_objects)
    except FileNotFoundError:
        print("\nFile not found")
        menu()

# captures a new product and writes it to inventory.txt
def capture_shoes():
    # ask user for the inputs and save them into variables
    # making sure that cost and quantity are numbers
    country = input("\nPlease enter the country\n")
    code = input("Please enter the SKU code\n")
    product = input("Please enter the product name\n")
    while True:
        cost = input("Please enter the cost of the product\n")
        if cost.isnumeric() == False:
            print("\nPlease enter a valid number")
        else:
            break
    while True:
        quantity = input("Please enter the quantity\n")
        if quantity.isnumeric() == False:
            print("\nPlease enter a valid number")
        else:
            break

    if quantity.isnumeric() == False:
        print("Please enter a valid number")

    # add the entries as objects into the shoes_objects list
    shoes_objects.append(Shoe(country, code, product, cost, quantity))

    # append the new object into inventory.txt
    with open("inventory.txt", "a") as file:
        # new_product is the last shoe object in the shoes_objects list
        new_product = shoes_objects[len(shoes_objects)-1]
        # write to the inventory.txt file and display a success message
        file.write("\n" + new_product.country + "," + new_product.code + "," + new_product.product + "," + new_product.cost + "," + new_product.quantity)
        print("\nNew product successfully captured and writen to file.")

    menu()

def view_all():
    # intialise the shoe_list and new_list lists
    shoe_list = []
    new_list = []

    # loop through the shoes_objects (via read_shoes_data())
    # list each object using the __str__() method
    for shoe in read_shoes_data():
        shoe_list.append(shoe.__str__())
    
    # loop through the shoe_list
    # strip and split
    # add the temp to the new_list list so it can be used in the tabulate function
    for shoe in (shoe_list):
        temp = shoe.strip()
        temp = temp.split(",")
        new_list.append(temp)
    
    # display results in table
    head = ["COUNTRY", "SKU CODE", "PRODUCT", "COST", "QUANTITY"]
    print(tabulate(new_list, headers=head, tablefmt="grid"))

    menu()

def re_stock():
    # assign the value returned from read_shoes_data() into shoes_objects
    # intialise quantity_list
    shoes_objects = (read_shoes_data())
    quantity_list = []

    # loop through shoes_objects (via read_shoes_data())
    # add the quantities to the quantity list
    for shoe in read_shoes_data():
        quantity_list.append(int(shoe.quantity))
    
    # find out the smallest value and save to variable
    smallest = min(quantity_list)
    
    # loop through the shoes_objects
    for shoe in shoes_objects:
        # find the product that has the smallest quantity
        if int(shoe.quantity) == smallest:
            # ask if user would like to restock and ask how many items they would like to add
            while True:
                restock = input(f"\nThere's only {shoe.quantity} left of product {shoe.code}.\nWould you like to re-stock this product(y/n)?\n")
                if restock.lower() == "y":
                    try:
                        more = int(input("\nHow many more items would you like to add?\n"))
                        # calculate the new quantity
                        new_quantity = int(shoe.quantity) + more
                        shoe.quantity = str(new_quantity)

                        # write the updated shoes_objects to the inventory.txt file
                        with open("inventory.txt", "w") as file:
                            for item in shoes_objects:
                                new_line =  item.country + "," + item.code + "," + item.product + "," + item.cost + "," + item.quantity + "\n"
                                file.writelines(new_line)

                        # display a message to user showing the updated quantity
                        print(f"\nThere are now {shoe.quantity} " + "x" + f" {shoe.code} in stock")
                        menu()
                    except ValueError:
                        print("\nincorrect input")
                        break
                elif restock.lower() == "n":
                    menu()
                else:
                    print("\nincorrect input")
    menu()

# search a product by SKU code
def search_shoe():
    # ask user to enter the code and save to shoe_code
    shoe_code = input("\nPlease enter the product code you would like to check\n")

    # loop through shoes_objects list (via read_shoes_data()) and display requested object
    for shoe in read_shoes_data():
        if shoe.code == shoe_code:
            print(shoe.__str__())
            menu()
    print("\nProduct does not exist")
    menu()

# calculate total value of all the items for a particular product
def value_per_item():
    # intialise lists
    total_cost = []
    new_list = []
    
    # loop through shoes_objects via (read_shoes_data())
    # calulate the total value of all items of each product
    # add the code and total for each product to a list
    for shoe in read_shoes_data():
        total = int(shoe.cost) * int(shoe.quantity)
        total_cost.append(shoe.code + "," + str(total))

    # loop through total_cost
    # strip and split
    # add to new_list
    for item in total_cost:
        temp = item.strip()
        temp = temp.split(",")
        new_list.append(temp)

    # display sku codes and total values in a table
    head = ["SKU CODE", "TOTAL VALUE"]
    print(tabulate(new_list, headers=head, tablefmt="grid"))
    
    menu()

def highest_qty():
    # intialise quantity_list
    quantity_list = []

    # loop through shoes_objects (via read_shoes_data())
    # add all the quantities of each object to a list
    for shoe in read_shoes_data():
        quantity_list.append(int(shoe.quantity))

    # find highest quantity and assign the value to a variable
    highest = max(quantity_list)

    # loop through shoes_objects (via read_shoes_data())
    # find the objects that have the highest quantities and display a message showing that the shoe is for sale
    for shoe in read_shoes_data():
        if int(shoe.quantity) == highest:
            print(f"\n{shoe.code} - {shoe.product} is for sale")

    menu()

def menu():
    # initialise user_choice to empty string
    user_choice = ""

    while user_choice != "quit":
        # display menu to user and save his choice in user_choice
        user_choice = input("\nWhat would you like to do?\n\nva   - View All Shoes?\ncc   - Check Cost?\ncq   - Check Quantity\ncs   - Capture Shoes\nrs   - re-stock\nss   - Search Shoe\nvpi  - Value Per Item\nhq   - Highest Quantity\nquit - Quit\n")
        if user_choice == "va":
            view_all()
            break
        if user_choice == "cc" or user_choice == "cq":
            # ask user for the SKU code and save as shoe_code
            shoe_code = input("\nPlease enter the SKU code you would like to check\n")
            # loop through shoes_objects via (read_shoes_data())
            # find the object with the matching SKU code
            # call either get_cost or get_quantity based on user_choice
            for shoe in read_shoes_data():
                if shoe_code == shoe.code:
                    if user_choice == "cc":
                        shoe.get_cost()
                        menu()
                    else:
                        shoe.get_quantity()
                        menu()
            print("\nSKU code not found")
            menu()
        if user_choice == "cs":
            capture_shoes()
            break           
        if user_choice == "rs":
            re_stock()
            break    
        if user_choice == "ss":
            search_shoe()
            break
        if user_choice == "vpi":
            value_per_item()
            break  
        if user_choice == "hq":
            highest_qty()
            break           
        elif user_choice == "quit":
            exit()
        else:
            print("\nOops - incorrect input")

menu()