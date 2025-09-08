import json
from accounts import SavingsAccount, CheckingAccount, OverdraftAccount

SAVE_FILE = "bank_data.json"


def download_accounts(accounts):
    data = {}
    for  name, acc in accounts.items():
        print(f"raw data for {name}: {acc}")
        acc_type = acc["type"]
        if acc_type == "SavingsAccount":
            data[name] = {
            "type": acc["type"],
            "owner": name,
            "balance": acc["balance"],
            "pin": acc["pin"],
            "extra": {
                "interest_rate": acc["interest_rate"],
            },
            "transactions": getattr(acc, "transactions", [])
            }
        elif acc_type == "CheckingAccount":
            data[name] = {
            "type": acc["type"],
            "owner": acc.get("owner", name),
            "balance": acc["balance"],
            "pin": acc["pin"]
            }
        elif acc_type == "OverdraftAccount":
            data[name] = {
            "type": acc["type"],
            "owner": acc.get("owner", name),
            "balance": acc["balance"],
            "pin": acc["pin"],
            "extra": {
                "overdraft": acc["overdraft"],
            },
            "transactions": getattr(acc, "transactions", [])
            }
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=4)
    print(" Accounts saved.")


def upload_accounts():
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

        # ✅ Store object back into dict
        accounts[name] = acc

    print(" Accounts loaded.")
    return accounts