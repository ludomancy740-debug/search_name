import getpass
import data
import test_accounts
from accounts import SavingsAccount, CheckingAccount, OverdraftAccount, LoggingMixin, LoggingCheckingAccount, LoggingOverdraftAccount, LoggingSavingsAccount
from helpers import get_amount, verify_account
from config import DEFAULT_INTEREST_RATE, DEFAULT_OVERDRAFT

accounts = {}

#----- Operations -----#
def create_account():
    owner = input("Enter name: ").strip().title()
    pin = getpass.getpass("Set a 4-digit PIN: ").strip()
    acc_type = input("Account Type (savings/checking/overdraft): ").strip().lower()

    if acc_type == "savings":
        new_acc = SavingsAccount(owner, 0, pin, DEFAULT_INTEREST_RATE)
    elif acc_type == "checking":
        new_acc = CheckingAccount(owner, 0, pin)
    elif acc_type == "overdraft":
        new_acc = OverdraftAccount(owner, 0, pin, DEFAULT_OVERDRAFT)
    else:
        print("Unknown account type. Defaulting to SavingsAccount.")
        new_acc = SavingsAccount(owner, 0, pin, DEFAULT_INTEREST_RATE)

    accounts[owner] = new_acc
    print(f"Account created for {owner} ({acc_type})!")


def update_account():
    name = input("Enter Account Name: ").strip().title()
    account = verify_account(accounts, name)
    if not account:
        return
    action = input("Deposit (D) / Withdraw (W) / Interest (I): ").strip().lower()

    if action in ["deposit", "d"]:
        amount = get_amount("Enter amount to deposit: £")
        account.deposit(amount)
    elif action in ["withdraw", "w"]:
        amount = get_amount("Enter amount to withdraw: £")
        account.withdraw(amount)
    elif action in ["interest", "i"]:
        if hasattr(account, "add_interest"):
            account.add_interest()
        else:
            print("Interest only available for Savings Accounts.")


def delete_account():
    name = input("Please Enter account name to delete: ").strip().title()
    if name in accounts:
        confirm = input(f"Confirm account deletion of {name}? (y/n): ").lower()
        if confirm == "y":
            del accounts[name]
            print(f"{name}'s account deleted.")
        else:
            print("Cancelled.")
    else:
        print("Account not found.")


def view_accounts():
    if not accounts:
        print("No accounts available.")
        return
    for acc in accounts.values():
        acc.show_balance()

def view_transactions():
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


def load_accounts():
    for name, info in data.accounts.items():
        acc_type = info["type"]
        if acc_type == "CheckingAccount":
            accounts[name] = CheckingAccount(name, info["balance"], info["pin"])
        elif acc_type == "SavingsAccount":
            accounts[name] = SavingsAccount(name, info["balance"], info["pin"], info.get("interest_rate"))
        elif acc_type == "OverdraftAccount":
            accounts[name] = OverdraftAccount(name, info["balance"], info["pin"], info.get("overdraft"))
    print("Accounts loaded (Alice, Bob, Charles, Dave).")
def load_test_accounts():
    for name, info in test_accounts.test_accounts.items():
        print(f"loading {name} debug account...")
        acc_type = info["type"]
        if acc_type == "CheckingAccount":
            accounts[name] = LoggingCheckingAccount(name, info["balance"], info["pin"])
        elif acc_type == "SavingsAccount":
            accounts[name] = LoggingSavingsAccount(name, info["balance"], info["pin"], info.get("interest_rate"))
        elif acc_type == "OverdraftAccount":
            accounts[name] = LoggingOverdraftAccount(name, info["balance"], info["pin"], info.get("overdraft"))
    print("Debug Test accounts loaded (Alice Test, Bob Test, Charles Test, Dave Test).")