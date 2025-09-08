test_accounts =  {
    "Alice Test":  {"type": "CheckingAccount", "balance": 300, "pin": "0000"},
    "Bob Test": {"type": "CheckingAccount", "balance": 400, "pin": "0000"},
    "Charles Test": {"type": "SavingsAccount", "balance": 100, "pin": "0000", "interest_rate": 0.05},
    "Dave Test": {"type": "OverdraftAccount", "balance": 200, "pin": "0000", "overdraft": 1000},
    }


def load_debug_accounts():
    print("Debug Test accounts loaded (Alice, Bob, Charles, Dave).")