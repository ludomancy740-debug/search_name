import json
import config
from accounts import SavingsAccount, CheckingAccount, OverdraftAccount

#Change storage based on debug
if config.DEBUG:
    SAVE_FILE = "bank_data.json"
else:
    SAVE_FILE = "test_bank_data.json"
    

def save_accounts(accounts):
    data = {}
    for name, acc in accounts.items():
        acc_data = {
            "type": acc.__class__.__name__,
            "owner": acc.owner,
            "balance": acc._balance,
            "pin": acc._pin,
            "transactions": getattr(acc, "transactions", [])
        }
        if isinstance(acc,SavingsAccount):
            acc_data["extra"] = {"interest_rate": acc.interest_rate}    
        elif isinstance(acc,OverdraftAccount):
            acc_data["extra"] = {"overdraft": acc.overdraft}
        data[name] = acc_data
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=4)
    print(" Accounts saved.")


def load_accounts():
    try:
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

    accounts = {}
    for name, acc_data in data.items():
        acc_type = acc_data["type"]

        #  REBUILD into real class instance
        if acc_type == "SavingsAccount":
            acc = SavingsAccount(
                acc_data["owner"],
                acc_data["balance"],
                acc_data["pin"],
                acc_data["extra"].get("interest_rate", 0.02)
            )
        elif acc_type == "CheckingAccount":
            acc = CheckingAccount(
                acc_data["owner"],
                acc_data["balance"],
                acc_data["pin"]
            )
        elif acc_type == "OverdraftAccount":
            acc = OverdraftAccount(
                acc_data["owner"],
                acc_data["balance"],
                acc_data["pin"],
                acc_data["extra"].get("overdraft", 0)
            )
 

        # Restore transactions if present
        acc.transactions = acc_data.get("transactions", [])

        # Store object back into dict
        accounts[name] = acc
        print(f"{name}'s account added.")

    print(" Accounts loaded.")
    return accounts