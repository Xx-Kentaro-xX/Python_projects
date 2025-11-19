import sys
from menu import MENU

resources = {
    "water": 300,
    "milk": 200,
    "coffee": 100,
    "money": 0
}


#1. Ask user to input order
#2. Turn off coffee machine when "off" entered on prompt
def ask_order():
    '''
    Ask user to input their order on prompt, then ..
    ・If input value is matched any value from menu, then return it
    ・If 'off' input as input value, then print turn off message and close process
    ・If 'report' input as input value, then call report_output()
    '''

    order = input("What would you like? (espresso/latte/cappuccino): ").lower()


    valid_menus = list(MENU.keys())
    valid_menus.append("off") # Add 'off' as valid input to trigger turn off function
    valid_menus.append("report") # Add 'report' as valid input output remaining resources

    # Order validity Check
    if order in valid_menus: # Valid case
        return order

    else: # Invalid case
        print("Invalid menu input. Please start over.")
        sys.exit()

#3. Print resources(remaining water, milk, coffee and money) when user entered "report" on prompt
def report_output():
    '''Print remaining resources'''
    #Print resource information
    for key in resources.keys():
        if (key == "water") or (key == "milk"):
            print(f"{key} : {resources[key]}ml")
        elif key == "coffee":
            print(f"{key} : {resources[key]}g")
        else:
            print(f"{key} : ${resources[key]}")


#4. Check whether remaining resources are enough to serve ordered product
def ingredients_check(order):
    '''
    Receive ordered menu and check whether remaining resources are enough to serve it.
    ・Enough resources => return True to proceed to next step
    ・Not Enough resources => print message and return False
    '''
    required_ingredients = MENU[order]["ingredients"]
    resource_passed_flg = True
    failed_ingredient = ""


    #Resouece check
    for ingredient in required_ingredients.keys():
        if resources[ingredient] < required_ingredients[ingredient]:
            resource_passed_flg = False
            failed_ingredient = ingredient

    if resource_passed_flg: # If all resources passed check, go to coin check
        return True

    else: # If resources couldn't pass check, then update remaining resources
        print(f"Sorry we don't have enough {failed_ingredient}")
        return False

#5. Ask user to insert coins
def coin_insertion():
    '''Ask user to insert coins and return total inserted price.'''
    total = 0

    total += 0.25 * int(input("How many quarters? : "))
    total += 0.1 * int(input("How many dimes? : "))
    total += 0.05 * int(input("How many nickles? : "))
    total += 0.01 * int(input("How many pennies? : "))

    # print(total) #test purpose

    return total


#6. Check transaction(Payment) can be done successfully
#7. Make coffee
def price_check(order, money):
    '''
    Check user inserted coins price is enough to order the menu
    ・Enough coins => print return change and server menu messages
    ・Not enough coins => print refund message
    '''

    required_price = MENU[order]["cost"]

    if money > required_price: #Enough money inserted case

        #update resources
        update_resources(order)

        print(f"Here is ${round(money - required_price, 2)} in charge.")
        print(f"Here is your {order.capitalize()} ☕️. Enjoy!")
    else:
        print("Sorry that's not enough money. Money refunded")


#6.5 Update resources
def update_resources(order):
    '''Update resource(global variable) values based on passed order value'''
    #Add money
    earned_money = MENU[order]["cost"]
    resources["money"] += earned_money

    #Reduce ingredients
    ingredients_list = MENU[order]["ingredients"].keys()

    for ingredient in ingredients_list:
        resources[ingredient] -= MENU[order]["ingredients"][ingredient]

    # print(resources) #test purpose


def main():

    continue_flg = True

    #Continue order unless user input invalid order or "off"
    while continue_flg:

        order = ask_order() #Store user input value for "order"

        #If user input "off", then print turn off message and close process
        if order == "off":
            print("Machine turned off..")
            continue_flg = False
            break

        elif order == "report":
            report_output()

        else:
            #Store T or F to identify whether having enough resources for "menu_prepare_check_flg"
            menu_prepare_check_flg = ingredients_check(order)

            if menu_prepare_check_flg: #Resource check passed case
                inserted_money = coin_insertion()

                #Price check
                price_check(order, inserted_money)


main()
