import config

from bank import create_account, view_accounts, update_account, delete_account, view_transactions
from storage import save_accounts, load_accounts
from mixins import LoggingMixin



#test_accounts = load_test_accounts()
def main_menu():
    accounts = {}
    while True:
        print("\n" + "="*30)
        print("        BANK SYSTEM MENU")
        print("="*30)
        if config.DEBUG:
            print("Debug Mode: ON")
        else:
            print("Debug Mode: OFF")
        print("Press 'L' to load accounts")
        print("Press 'T' to load test accounts")
        print("1. Create Account")
        print("2. View All Accounts")
        print("3. View Transactions")
        print("4. Update Account")
        print("5. Delete Account")
        print("6. Toggle Debug (Currently: " + ("ON" if config.DEBUG else "OFF") + ")")
        if config.DEBUG:
            print("7. Toggle Logs (Currently: " + ("ON" if LoggingMixin.logging_enabled else "OFF") + ")")
            print("8. Load Debug Accounts")
            print("9. Quit")
        else:
            print("7. Quit")
        print("="*30)

        choice = input("Choice: ").strip().lower()
        if choice == "1":
            create_account()
        elif choice == "2":
            view_accounts(accounts)
        elif choice == "3":
            view_transactions(accounts)
        elif choice == "4":
            update_account(accounts)
        elif choice == "5":
            delete_account(accounts)
        elif choice == "6":
            config.DEBUG = not config.DEBUG
            print("Debug mode is now " + ("ON" if config.DEBUG else "OFF"))
        elif config.DEBUG and choice == "7":
            LoggingMixin.logging_enabled = not LoggingMixin.logging_enabled
        elif config.DEBUG and choice == "8":
            print("To Be Implemented....")
        elif (config.DEBUG and choice == "9") or (not config.DEBUG and choice == "7") or choice in ["7", "q", "quit"]:
            if config.DEBUG:
                #download_accounts(test_accounts)
                print("To Be Implemented....")
            else:
                save_accounts(accounts)
            print("Exiting program...")
            break
        elif choice == "l":
            accounts = load_accounts()
        elif choice == "t":
            print("To Be Implemented....")
            #print((" Loaded Test Accounts!"))
        else:
            print("Invalid option, try again.")


if __name__ == "__main__":
    main_menu()

