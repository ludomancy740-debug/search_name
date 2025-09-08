#----- Bank Data -----
accounts = {
    "Alice": {
        "type": "CheckingAccount",
        "balance": 200,
        "pin": "0000"
    },
    "Bob": {
        "type": "CheckingAccount",
        "balance": 100,
        "pin": "0000"
    },
    "Charles": {
        "type": "SavingsAccount",
        "balance": 50,
        "pin": "0000",
        "interest_rate": 0.05
    },
    "Dave": {
        "type": "OverdraftAccount",
        "balance": 20,
        "pin": "0000",
        "overdraft": 1000
    }
}