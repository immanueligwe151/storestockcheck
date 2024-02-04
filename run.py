import gspread
from google.oauth2.service_account import Credentials
import maskpass

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('stockcount')

def return_previous_day_sales():
    #this function fetches the previous day's sales from the Google worksheet and returns it where required
    worksheet = SHEET.worksheet('sales_sheet')
    data = worksheet.get_all_values()
    return data[len(data) - 1] # retrieves the last line from the sheet, which is the day's previous sales

def append_new_sales(data):
    #this function adds the current day's sales to the Google worksheet
    worksheet = SHEET.worksheet('sales_sheet')
    worksheet.append_row(data)
    print("The sales for today have been added to the Google sheets for future use")

def amount_input(item, itemtype):
    '''
        This is to deal with the input that is to be made the user. As there are several parts of the program where
        the user input is handled in a similar manner, this function exists to avoid rewriting code to do the exact
        same thing over and over, and input validation is also included in this
    '''
    valid = False
    data = 0.0 # set a default value for data
    print()
    while (not valid):
        try:
            if (itemtype == "itemsold"):
                data = input("Number of " + item + " sold today:  \n")
            elif (itemtype == "bagsleft"):
                data = input("Number of bags of " + item + " remaining:  \n")
            elif (itemtype == "looseleft"):
                data = input("Number of loose " + item + " remaining:  \n")
            int(data) 
        except:
            print("Invalid, please enter a numerical value.")
        else:
            valid = True
    return data

def defrost_quantities(previous, sold, bag, loose, held_in_bag):
    '''
        This calculates how much product should be brought out for defrost. The program will compare how much was sold
        the previous day and how much was sold on the current day. Depending on which is more, the program will then
        determine how much defrost to put in, taking away the defrosted amount on hold from the eventual total.
    '''
    new_defrost = 0
    total_held = (bag * held_in_bag) + loose #the total of the product on hand
    if (previous > sold):
        new_defrost = previous + total_held
        #if more was sold the previous day, we would take the product we have on hand and add it from the total sold yesterday
    else:
        new_defrost = sold + total_held + (held_in_bag * 2)
        #if more was sold today, we would take the number of product sold and add it to what's left, as well as 2 extra bags
    new_defrost = new_defrost / held_in_bag #converts to bags as it is currently in loose numbers
    return str(int(new_defrost))

def login():
    print("Welcome manager, please log in to continue:")
    logged_in = False
    while (logged_in == False):
        user_name = input("Username:  \n")
        password = maskpass.askpass(prompt="Password:  \n", mask="")
        if (user_name == "kfcmanager1" and password == "fngerlickch1ckn"):
            print("You have succesfully logged in.\n\n")
            logged_in = True
        else:
            print("Username or password is incorrect, please try again.\n")
    return logged_in

def view_sales():
    previous_sales = return_previous_day_sales()
    print("\n\nThese are the sales from yesterday:")
    print("Mini fillets: £" + previous_sales[0])
    print("Fillets: £" + previous_sales[1])
    print("Zingers: £" + previous_sales[2])
    print("Hot wings: £" + previous_sales[3])
    print("\nTotal sales: £" + str(float(previous_sales[0]) + float(previous_sales[1]) + float(previous_sales[2]) + float(previous_sales[3])))
    print()
    manager_menu()

def calculate_defrost():
    previous_sales = return_previous_day_sales()
    previous_minis = float(previous_sales[0]) / float(1.25)
    previous_fillets = float(previous_sales[1]) / float(3.0)
    previous_zingers = float(previous_sales[2]) / float(3.0)
    previous_hotwings = float(previous_sales[3]) / float(1.05)
    #the number of product sold on the previous day

    sold_minis = amount_input("mini fillets", "itemsold")
    sold_fillets = amount_input("fillets", "itemsold")
    sold_zingers = amount_input("zingers", "itemsold")
    sold_hotwings = amount_input("hot wings", "itemsold")

    bags_minis = int(amount_input("mini fillets", "bagsleft")) * 40
    bags_fillets = int(amount_input("fillets", "bagsleft")) * 20
    bags_zingers = int(amount_input("zingers", "bagsleft")) * 20
    bags_hotwings = int(amount_input("hot wings", "bagsleft")) * 65
    #multiplying the bags by the number of product in them to add to the total amount of product

    loose_minis = amount_input("mini fillets", "looseleft")
    loose_fillets = amount_input("fillets", "looseleft")
    loose_zingers = amount_input("zingers", "looseleft")
    loose_hotwings = amount_input("hot wings", "looseleft")
    #loose pieces of product that will eventually be added with those in the bags

    sales_minis = str(float(sold_minis) * 1.25)
    sales_fillets = str(int(sold_fillets) * 3)
    sales_zingers = str(int(sold_zingers) * 3)
    sales_hotwings = str(int(sold_hotwings) * 3)
    #calculates how much sales have been made; not taking in user input of sales so as to avoid error

    print()
    print("\nYou are to defrost " + defrost_quantities(int(previous_minis), int(sold_minis), int(bags_minis), int(loose_minis), 40) + " bags of mini fillets.")
    print("\nYou are to defrost " + defrost_quantities(int(previous_fillets), int(sold_fillets), int(bags_fillets), int(loose_fillets), 20) + " bags of fillets.")
    print("\nYou are to defrost " + defrost_quantities(int(previous_zingers), int(sold_zingers), int(bags_zingers), int(loose_zingers), 20) + " bags of zingers.")
    print("\nYou are to defrost " + defrost_quantities(int(previous_hotwings), int(sold_hotwings), int(bags_hotwings), int(loose_hotwings), 65) + " bags of hot wings.")

    append_new_sales([sales_minis, sales_fillets, sales_zingers, sales_hotwings])
    print("\n\n")
    manager_menu()


def manager_menu():
    print("Welcome to the Admin Manager Menu!\nPlease choose from the following options by typing in the relevant number:")
    print("1. Check yesterday's sales\n2. Calculate defrost for tomorrow\n3. Quit")
    valid = False
    while(not valid):
        selected_option = input("\nPlease select an option: \n")
        if (selected_option == "1"):
            view_sales()
            valid = True
        elif (selected_option == "2"):
            calculate_defrost()
            valid = True
        elif (selected_option == "3"):
            valid = True
            print("Thank you, bye for now!")
            quit()
        else:
            print("You've selected an invalid option, please select 1, 2 or 3.")

#this shows the login page first when the program loads
if (login()):
    manager_menu()
