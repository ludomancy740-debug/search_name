import getpass

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
