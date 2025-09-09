import config

from bank import create_account, view_accounts, update_account, delete_account, view_transactions, login
from storage import save_accounts, load_accounts
from mixins import LoggingMixin
from config import APP_RUNNING

#Startup Menu
def main_menu(accounts):
    global APP_RUNNING
    while APP_RUNNING:
        print("\n" + "="*30)
        print("            MAIN MENU")
        print("="*30)
        print("1. Login")
        print("2. Quit")
        choice = input("Choice: ").strip()

        if choice == "1":
            role, user = login(accounts)
            if role == "ADMIN":
                admin_menu(accounts)
            if role == "USER":
                user_menu(accounts, user)
        elif choice == "2":
            print("Exiting...")
            APP_RUNNING = False
            break
        else:
            print("Invalid option.")

#Main banking system menu (requires login first).
def user_menu(accounts, user):    
    print("\n=== Welcome to the Bank System ===")
    global APP_RUNNING
    while APP_RUNNING:
        print("\n" + "="*30)
        print(f"  Logged in as: {user.owner}")
        print("="*30)
        print("1. View My Account")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Transactions")
        print("5. Logout")
        print("6. Quit")
        print("="*30)

        choice = input("Choice: ").strip().lower()

        if choice == "1":
            user.show_balance()
        elif choice == "2":
            amount = int(input("Enter deposit amount: £"))
            user.deposit(amount)
        elif choice == "3":
            amount = int(input("Enter withdraw amount: £"))
            user.withdraw(amount)
        elif choice == "4":
            print("Transactions:")
            for t in user.transactions:
                if isinstance(t, dict):
                    trans_type = t.get("action", "Unknown")
                    amount = t.get("amount", 0)
                    time = t.get("time","Uknown")
                    print(f" - {time}: {trans_type} of £{amount}")
                else:
                    print(f"  - {t}")
        elif choice == "5":
            print("Logging out...")
            return
        elif choice in ["6", "q", "quit"]:
            print("Exiting...")
            save_accounts(accounts)
            APP_RUNNING = False
            break
        else:
            print("Invalid option.")


#Admin Menu
def admin_menu(accounts):
    global APP_RUNNING
    while APP_RUNNING:
        print("\n" + "="*30)
        print("        BANK SYSTEM MENU")
        print("="*30)
        if config.DEBUG:
            print("Debug Mode: ON")
        else:
            print("Debug Mode: OFF")
        print("Press 'L' to load accounts")
        print("1. Create Account")
        print("2. View All Accounts")
        print("3. View Transactions")
        print("4. Update Account")
        print("5. Delete Account")
        print("6. Toggle Debug (Currently: " + ("ON" if config.DEBUG else "OFF") + ")")
        if config.DEBUG:
            print("7. Toggle Logs (Currently: " + ("ON" if LoggingMixin.logging_enabled else "OFF") + ")")
            print("8. Load Debug Accounts")
            print("9. Logout")
            print("10. Quit (Exit program)")
        else:
            print("7. Logout")
            print("8. Quit (Exit program)")
        print("="*30)

        choice = input("Choice: ").strip().lower()
        if choice == "1":
            create_account(accounts)
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
            accounts = load_accounts()
        elif (config.DEBUG and choice == "9") or (not config.DEBUG and choice == "7"):
            print("Exiting Menu...")
            return
        elif (config.DEBUG and choice == "10") or (not config.DEBUG and choice == "8") or choice in ["8", "q", "quit"]:
            if config.DEBUG:
                save_accounts(accounts)
            else:
                save_accounts(accounts)
            print("Exiting app, Saving Accounts...")
            APP_RUNNING = False
            break

        else:
            print("Invalid option, try again.")


