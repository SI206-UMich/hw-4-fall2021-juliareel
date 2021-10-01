
import unittest

# testing a git commit

# The Customer class
# The Customer class represents a customer who will order from the stalls.
class Customer: 
    # Constructor
    def __init__(self, name, wallet = 100):
        self.name = name
        self.wallet = wallet

    # Reload some deposit into the customer's wallet.
    def reload_money(self,deposit):
        self.wallet += deposit

    # The customer orders the food and there could be different cases   
    def validate_order(self, cashier, stall, item_name, quantity):
        if not(cashier.has_stall(stall)):
            print("Sorry, we don't have that vendor stall. Please try a different one.")
        elif not(stall.has_item(item_name, quantity)):  
            print("Our stall has run out of " + item_name + " :( Please try a different stall!")
        elif self.wallet < stall.compute_cost(quantity): 
            print("Don't have enough money for that :( Please reload more money!")
        else:
            bill = cashier.place_order(stall, item_name, quantity) 
            self.submit_order(cashier, stall, bill) 
    
    # Submit_order takes a cashier, a stall and an amount as parameters, 
    # it deducts the amount from the customer’s wallet and calls the receive_payment method on the cashier object
    def submit_order(self, cashier, stall, amount): 
        self.wallet = self.wallet - amount
        cashier.receive_payment(stall, amount)

    # The __str__ method prints the customer's information.    
    def __str__(self):
        return "Hello! My name is " + self.name + ". I have $" + str(self.wallet) + " in my payment card."


# The Cashier class
# The Cashier class represents a cashier at the market. 
class Cashier:

    # Constructor
    def __init__(self, name, directory =[]):
        self.name = name
        self.directory = directory[:] # make a copy of the directory

    # Whether the stall is in the cashier's directory
    def has_stall(self, stall):
        return stall in self.directory

    # Adds a stall to the directory of the cashier.
    def add_stall(self, new_stall):
        self.directory.append(new_stall)

    # Receives payment from customer, and adds the money to the stall's earnings.
    def receive_payment(self, stall, money):
        stall.earnings += money

    # Places an order at the stall.
	# The cashier pays the stall the cost.
	# The stall processes the order
	# Function returns cost of the order, using compute_cost method
    def place_order(self, stall, item, quantity):
        stall.process_order(item, quantity)
        return stall.compute_cost(quantity) 
    
    # string function.
    def __str__(self):

        return "Hello, this is the " + self.name + " cashier. We take preloaded market payment cards only. We have " + str(sum([len(category) for category in self.directory.values()])) + " vendors in the farmers' market."

## Complete the Stall class here following the instructions in HW_4_instructions_rubric
class Stall:
    
    # Constructor
    def __init__(self, name, inventory={}, cost = 7, earnings = 0):
        self.name = name
        self.inventory = inventory  #food is key, quantities are values
        self.cost = cost
        self.earnings = earnings
    
    # Takes the food name and the quantity. If the stall has enough food, 
    # it will decrease the quantity of that food in the inventory.
    def process_order(self, food_name, food_quantity):
        if self.has_item(food_name, food_quantity):
            self.inventory[food_name] -= food_quantity

    # Takes the food name and the quantity and returns True if there 
    # is enough food left in the inventory and False otherwise.
    def has_item(self, food_name, food_quantity):
        if food_name in self.inventory and self.inventory[food_name] >= food_quantity:
            return True
        else:
            return False

    # Takes the food name and the quantity. It will add the quantity to the 
    # existing quantity if the item exists in the inventory dictionary or create a new item in 
    # the inventory dictionary with the item name as the key and the quantity as the value.
    def stock_up(self, food_name, food_quantity):
        # if the food item exists as a key in the inventory, increase value by the quantity
        if food_name in self.inventory:
            self.inventory[food_name] += food_quantity

        # else; if the food item is not a key:
            # create a new item as a key in the dictionary and put the quantity as the value
        else: 
            self.inventory[food_name] = food_quantity

    # takes the quantity and returns the total for an order. 
    # Since all the foods in one stall have the same cost, 
    # you only need to know the quantity of food items that the customer has ordered.
    def compute_cost(self, food_quantity):
        return food_quantity * self.cost

    # returns a string with the information in the instance variables using the format shown below:
    #  “Hello, we are [NAME]. This is the current menu [INVENTORY KEYS AS LIST]. We charge $[COST] per item. We have $[EARNINGS] in total.”
    def __str__(self):
        return ("Hello, we are " + int(self.name) + ". This is the current menu " + str(list(self.inventory.keys())) + 
        ". We charge $" + int(self.cost) + "per item. We have $" + int(self.earnings) + " in total.")


class TestAllMethods(unittest.TestCase):
    
    def setUp(self):
        inventory = {"Burger":40, "Taco":50}
        self.f1 = Customer("Ted")
        self.f2 = Customer("Morgan", 150)
        self.s1 = Stall("The Grill Queen", inventory, cost = 10)
        self.s2 = Stall("Tamale Train", inventory, cost = 9)
        self.s3 = Stall("The Streatery", inventory)
        self.c1 = Cashier("West")
        self.c2 = Cashier("East")
        #the following codes show that the two cashiers have the same directory
        for c in [self.c1, self.c2]:
            for s in [self.s1,self.s2,self.s3]:
                c.add_stall(s)

	## Check to see whether constructors work
    def test_customer_constructor(self):
        self.assertEqual(self.f1.name, "Ted")
        self.assertEqual(self.f2.name, "Morgan")
        self.assertEqual(self.f1.wallet, 100)
        self.assertEqual(self.f2.wallet, 150)

	## Check to see whether constructors work
    def test_cashier_constructor(self):
        self.assertEqual(self.c1.name, "West")
        #cashier holds the directory - within the directory there are three stalls
        self.assertEqual(len(self.c1.directory), 3) 

	## Check to see whether constructors work
    def test_truck_constructor(self):
        self.assertEqual(self.s1.name, "The Grill Queen")
        self.assertEqual(self.s1.inventory, {"Burger":40, "Taco":50})
        self.assertEqual(self.s3.earnings, 0)
        self.assertEqual(self.s2.cost, 9)

	# Check that the stall can stock up properly.
    def test_stocking(self):
        inventory = {"Burger": 10}
        s4 = Stall("Misc Stall", inventory)

		# Testing whether stall can stock up on items
        self.assertEqual(s4.inventory, {"Burger": 10})
        s4.stock_up("Burger", 30)
        self.assertEqual(s4.inventory, {"Burger": 40})
        
    def test_make_payment(self):
		# Check to see how much money there is prior to a payment
        previous_custormer_wallet = self.f2.wallet
        previous_earnings_stall = self.s2.earnings
        
        self.f2.submit_order(self.c1, self.s2, 30)

		# See if money has changed hands
        self.assertEqual(self.f2.wallet, previous_custormer_wallet - 30)
        self.assertEqual(self.s2.earnings, previous_earnings_stall + 30)


	# Check to see that the server can serve from the different stalls
    def test_adding_and_serving_stall(self):
        c3 = Cashier("North", directory = [self.s1, self.s2])
        self.assertTrue(c3.has_stall(self.s1))
        self.assertFalse(c3.has_stall(self.s3)) 
        c3.add_stall(self.s3)
        self.assertTrue(c3.has_stall(self.s3))
        self.assertEqual(len(c3.directory), 3)


	# Test that computed cost works properly.
    def test_compute_cost(self):
        #what's wrong with the following statements?
        #can you correct them?
        self.assertEqual(self.s1.compute_cost(5), 50)
        self.assertEqual(self.s3.compute_cost(6), 42)
        # compute_cost is an object of the stall class, just takes food_quantity

	# Check that the stall can properly see when it is empty
    def test_has_item(self):
        # Set up to run test cases

        # Test to see if has_item returns True when a stall has enough items left
        # Please follow the instructions below to create three different kinds of test cases 
        # Test case 1: the stall does not have this food item: 
        self.assertFalse(self.s1.has_item('Blueberries', 10))

        # Test case 2: the stall does not have enough food item: 
        self.assertFalse(self.s1.has_item('Burger', 50))
        
        # Test case 3: the stall has the food item of the certain quantity: 
        self.assertTrue(self.s2.has_item('Taco', 10))

	# Test validate order
    def test_validate_order(self):
        # call validate order to see if the cashier in the function call can work the stall passed

		# case 1: test if a customer doesn't have enough money in their wallet to order
        self.f1.validate_order(self.c1, self.s1, 'Burger', 30)

		# case 2: test if the stall doesn't have enough food left in stock
        self.f2.reload_money(500)
        self.f2.validate_order(self.c2, self.s3, 'Burger', 50)

		# case 3: check if the cashier can order item from that stall
        self.s4 = Stall("Testing additional stall", {"Burger":40, "Taco":50})
        self.f2.validate_order(self.c2, self.s4, 'Taco', 5)

    # Test if a customer can add money to their wallet
    def test_reload_money(self):
        self.f1.reload_money(100)
    
### Write main function
def main():
    #Create different objects 

    # create at least two inventory dictionaries
    fruits = {'apple': 19, 
              'banana': 12, 
              'tomato': 5,
              'strawberry': 53}
    vegetables = {'carrot': 12,
                  'broccoli': 14,
                  'corn': 7}
    fruits_and_veggies = {'apple': 19, 
                          'banana': 12, 
                          'tomato': 5,
                          'strawberry': 53,
                          'carrot': 12,
                          'broccoli': 14,
                          'corn': 7}

    # create at least 3 customer objects
    cust1 = Customer('Steve', 153)
    cust2 = Customer('Linda', 84)
    cust3 = Customer('Jake', 13)

    # create at least 2 stall objects
    s1 = Stall('Fruit Stand', fruits, 8, 0)
    s2 = Stall('Vegetable Stand', vegetables, 5, 0)
    s3 = Stall('Fruits and Vegetables', fruits_and_veggies, 6, 0)
    
    # create at least 2 cashier objects
    cash1 = Cashier('Emily', [s1, s2])
    cash2 = Cashier('Ben', [s3])

    # have each customer place at least one order (by calling validate_order) 
    # and try all cases in the validate_order function above.

    #Try all cases in the validate_order function
    #Below you need to have *each customer instance* try the four cases
    #case 1: the cashier does not have the stall 
    cust1.validate_order(cash2, s1, 'apple', 5)
    cust2.validate_order(cash1, s3, 'corn', 2)
    cust3.validate_order(cash2, s2, 'broccoli', 8)
    
    #case 2: the casher has the stall, but not enough ordered food or the ordered food item
    cust1.validate_order(cash1, s1, 'tomato', 8)
    cust2.validate_order(cash2, s3, 'carrot', 15)
    cust3.validate_order(cash1, s2, 'apple', 8)
    
    #case 3: the customer does not have enough money to pay for the order: 
    cust1.validate_order(cash1, s1, 'strawberry', 22)
    cust2.validate_order(cash2, s3, 'banana', 12)
    cust3.validate_order(cash1, s2, 'carrot', 3)
    
    #case 4: the customer successfully places an order
    cust1.validate_order(cash2, s3, 'tomato', 4)
    cust2.validate_order(cash1, s1, 'banana', 3)
    cust3.validate_order(cash1, s2, 'carrot', 1)


if __name__ == "__main__":
	main()
	print("\n")
	unittest.main(verbosity = 2)
