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
    worksheet = SHEET.worksheet('sales_sheet')
    data = worksheet.get_all_values()
    return data[len(data) - 1] # retrieves the last line from the sheet, which is the day's previous sales

def append_new_sales(data):
    worksheet = SHEET.worksheet('sales_sheet')
    worksheet.append_row(data)
    print("The sales for today have been added to the Google sheets for future use")

def amount_input(item, itemtype):
    valid = False
    data = 0.0 # set a default value for data
    print()
    while (not valid):
        try:
            if (itemtype == "itemsold"):
                data = input("Number of " + item + " sold today:  ")
            elif (itemtype == "bagsleft"):
                data = input("Number of bags of " + item + " remaining:  ")
            elif (itemtype == "looseleft"):
                data = input("Number of loose " + item + " remaining:  ")
            float(data)
        except:
            print("Invalid, please enter a numerical value.")
        else:
            valid = True
    return data

def defrost_quantities(previous, sold, bag, loose):
    print("something")

def login():
    print("Welcome manager, please log in to continue:")
    logged_in = False
    while (logged_in == False):
        user_name = input("Username:  ")
        password = maskpass.askpass(prompt="Password:  ", mask="")
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
    manager_menu()

def calculate_defrost():
    previous_sales = return_previous_day_sales()
    previous_minis = float(previous_sales[0]) / float(1.25)
    previous_fillets = float(previous_sales[1]) / float(3.0)
    previous_zingers = float(previous_sales[2]) / float(3.0)
    previous_hotwings = float(previous_sales[3]) / float(1.05)

    sold_minis = amount_input("mini fillets", "itemsold")
    sold_fillets = amount_input("fillets", "itemsold")
    sold_zingers = amount_input("zingers", "itemsold")
    sold_hotwings = amount_input("hot wings", "itemsold")

    bags_minis = amount_input("mini fillets", "bagsleft")
    bags_fillets = amount_input("fillets", "bagsleft")
    bags_zingers = amount_input("zingers", "bagsleft")
    bags_hotwings = amount_input("hot wings", "bagsleft")

    loose_minis = amount_input("mini fillets", "looseleft")
    loose_fillets = amount_input("fillets", "looseleft")
    loose_zingers = amount_input("zingers", "looseleft")
    loose_hotwings = amount_input("hot wings", "looseleft")

    sales_minis = str(sold_minis * 1.25)
    sales_fillets = str(sold_fillets * 3)
    sales_zingers = str(sold_zingers * 3)
    sales_hotwings = str(sold_hotwings * 3)

    print()
    print("\nYou are to defrost " + defrost_quantities(previous_minis, sold_minis, bags_minis, loose_minis) + " bags of mini fillets.")
    print("\nYou are to defrost " + defrost_quantities(previous_fillets, sold_fillets, bags_fillets, loose_fillets) + " bags of fillets.")
    print("\nYou are to defrost " + defrost_quantities(previous_zingers, sold_zingers, bags_zingers, loose_zingers) + " bags of zingers.")
    print("\nYou are to defrost " + defrost_quantities(previous_hotwings, sold_hotwings, bags_hotwings, loose_hotwings) + " bags of minis.")

    append_new_sales([sales_minis, sales_fillets, sales_zingers, sales_hotwings])
    print("\n\n")
    manager_menu()


def manager_menu():
    print("Welcome to the Admin Manager Menu!\nPlease choose from the following options by typing in the relevant number:")
    print("1. Check yesterday's sales\n2. Calculate defrost for tomorrow")
    valid = False
    while(not valid):
        selected_option = input("\nPlease select an option: ")
        if (selected_option == "1"):
            view_sales()
            valid = True
        elif (selected_option == "2"):
            calculate_defrost()
            valid = True
        else:
            print("You've selected an invalid option, please select 1 or 2.")

if (login()):
    manager_menu()
