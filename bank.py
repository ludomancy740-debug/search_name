import getpass
from accounts import SavingsAccount, CheckingAccount, OverdraftAccount, LoggingMixin, LoggingCheckingAccount, LoggingOverdraftAccount, LoggingSavingsAccount
from helpers import get_amount, verify_account
from config import DEFAULT_INTEREST_RATE, DEFAULT_OVERDRAFT

accounts = {}

#----- Operations -----#
def create_account():
    owner = input("Enter name: ").strip().title()
    pin = getpass.getpass("Set a 4-digit PIN: ").strip()
    if len(pin) != 4 or not pin.isdigit():
        print("PIN must be 4 digits.")
        return
    acc_type = input("Account Type (normal/savings/checking/overdraft): ").strip().lower()
    if acc_type in ["savings", "s"]:
        new_acc = SavingsAccount(owner,0,pin,0.05)
    elif acc_type in ["checking", "c"]:
        new_acc = CheckingAccount(owner,0,pin)
    elif acc_type in ["overdraft", "o"]:
        new_acc = OverdraftAccount(owner,0,pin,overdraft=100)
    else:
        print("Invalid type, creating normal account.")
        new_acc = SavingsAccount(owner,0,pin)
    accounts[owner] = new_acc
    print(f"Account created for {owner} ({acc_type})!")


def update_account(accounts):
    name = input("Enter Account Name: ").strip().title()
    account = verify_account(accounts, name)
    if not account:
        return
    action = input("Deposit (D) / Withdraw (W) / Interest (I): ").strip().lower()
    if action in ["deposit", "d"]:
        amount = get_amount()
        account.deposit(amount)
    elif action in ["withdraw", "w"]:
        amount = get_amount()
        account.withdraw(amount)
    elif action in ["interest", "i"]:
        if isinstance(account, SavingsAccount):
            account.add_interest()
        else:
            print("Interest only available for Savings Accounts.")

def delete_account(accounts):
    name = input("Enter account name to delete: ").strip().title()
    if name in accounts:
        confirm = input(f"Confirm deletion of {name}? (y/n): ").lower()
        if confirm == "y":
            del accounts[name]
            print(f"{name}'s account deleted.")
    else:
        print("Account not found.")

#----- Operations -----#
def view_accounts(accounts):
    if not accounts:
        print("No accounts available.")
        return
    for acc in accounts.values():
        acc.show_balance()

def view_transactions(accounts):
    name = input("Enter Account Name: ").strip().title()
    account = verify_account(accounts, name)
    if not account:
        return
    if not account.transactions:
        print("No transactions yet.")
        return
    print(f"\nTransaction history for {name}:")
    for t in account.transactions:
        print(f"{t['time']} | {t['action']} £{t['amount']} | Balance: £{t['balance']}")


#--- Helper functions ---#
def verify_account(accounts, name):
    if name not in accounts:
        print("Account not found.")
        return None
    pin = getpass.getpass("Enter PIN: ").strip()
    if accounts[name].check_pin(pin):
        return accounts[name]
    else:
        print("Incorrect PIN.")
        return None

def get_amount(prompt="Enter amount: £"):
    while True:
        try:
            amount = int(input(prompt))
            if amount <= 0:
                print("Amount must be greater than zero.")
                continue
            return amount
        except ValueError:
            print("Please enter a valid number.")

