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

def login():
    print("Welcome manager, please log in to continue:")
    logged_in = False
    while (logged_in == False):
        user_name = input("Username: ")
        password = maskpass.askpass(prompt="Password: ", mask="")
        if (user_name == "kfcmanager1" and password == "fngerlickch1ckn"):
            print("You have succesfully logged in.\n\n")
            logged_in = True
        else:
            print("Username or password is incorrect, please try again.\n")
    return logged_in

def view_sales():
    print("this")

def calculate_defrost():
    print("also this")

def manager_menu():
    print("Welcome to the Admin Manager Menu!\nPlease choose from the following options by typing in the relevant number:")
    print("1. Check yesterday's sales\n2. Calculate defrost for tomorrow")
    while(False):
        selected_option = input("\nPlease select an option: ")
        if (selected_option == "1"):
            view_sales()
        elif (selected_option == "2"):
            calculate_defrost()
        else:
            print("You've selected an invalid option, please select 1 or 2.")
            continue

if (login()):
    manager_menu()
