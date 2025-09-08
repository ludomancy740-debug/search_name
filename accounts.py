from abc import ABC, abstractmethod
from config import DEFAULT_INTEREST_RATE, CHECKING_FEE, DEFAULT_OVERDRAFT
from mixins import LoggingMixin
from datetime import datetime
class BankAccount(ABC):
    def __init__(self, owner, balance, pin="0000"):
        self.owner = owner
        self._balance = balance
        self._pin = pin
        self.transactions = []

    def check_pin(self, pin):
        return self._pin == pin

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            print(f"[{self.owner}] Deposited £{amount}. New Balance: £{self._balance}")
        else:
            print("Deposit must be greater than zero!")

    @abstractmethod
    def withdraw(self, amount):
        pass

    def show_balance(self):
        print(f"Owner: {self.owner} | Balance: £{self._balance}")

    def record_transaction(self, action, amount=0):
        self.transactions.append({

            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "action": action,
            "amount": amount,
            "balance": self._balance
        })


class SavingsAccount(BankAccount):
    def __init__(self, owner, balance=0, pin="0000", interest_rate=DEFAULT_INTEREST_RATE):
        super().__init__(owner, balance, pin)
        self.interest_rate = interest_rate

    def withdraw(self, amount):
        if amount <= self._balance:
            self._balance -= amount
            print(f"[{self.owner}] Withdrew £{amount}. New Balance: £{self._balance}")
            self.record_transaction("Withdraw", amount)
        else:
            print("Insufficient funds. Balance: £{self._balance}")

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            print(f"[{self.owner}] Deposited £{amount}. New Balance: £{self._balance}")
            self.record_transaction("Deposit", amount)
        else:
            print("Deposit must be greater than zero!")

    def add_interest(self):
        interest = self._balance * self.interest_rate
        self._balance += interest
        print(f"[{self.owner}] Added £{interest:.2f} interest. New Balance: £{self._balance}")
        self.record_transaction("Interest ", interest)


class CheckingAccount(BankAccount):
    def withdraw(self, amount):
        if amount + CHECKING_FEE <= self._balance:
            self._balance -= (amount + CHECKING_FEE)
            print(f"[{self.owner}] Withdrew £{amount} + £{CHECKING_FEE} fee. New Balance: £{self._balance}")
            self.record_transaction("Withdraw", amount)
        else:
            print("Insufficient funds (including fee).")


class OverdraftAccount(BankAccount):
    def __init__(self, owner, balance=0, pin="0000", overdraft=DEFAULT_OVERDRAFT):
        super().__init__(owner, balance, pin)
        self.overdraft = overdraft

    def withdraw(self, amount):
        if self._balance - amount >= -self.overdraft:
            self._balance -= amount
            print(f"[{self.owner}] Withdrew £{amount}. New Balance: £{self._balance}")
            self.record_transaction("Withdraw", amount)
        else:
            print(f"Overdraft limit reached. Balance: £{self._balance}, Limit: -£{self.overdraft}")

# ========== Combined Classes (Mixin + Subclass) ==========
class LoggingSavingsAccount(SavingsAccount, LoggingMixin):
    def deposit(self, amount):
        super().deposit(amount)
        self.log(f"Deposited {amount}")
        self.record_transaction("[LOG] Deposit", amount)

    def withdraw(self, amount):
        super().withdraw(amount)
        self.log(f"Tried to withdraw £{amount}")
        self.record_transaction("[LOG] Withdraw", amount)


class LoggingCheckingAccount(CheckingAccount, LoggingMixin):
    def deposit(self, amount):
        super().deposit(amount)
        self.log(f"Deposited £{amount}")
        self.record_transaction("[LOG] Deposit", amount)

    def withdraw(self, amount):
        super().withdraw(amount)
        self.log(f"Tried to withdraw £{amount}")
        self.record_transaction("[LOG] Withdraw", amount)


class LoggingOverdraftAccount(OverdraftAccount, LoggingMixin):
    def deposit(self, amount):
        super().deposit(amount)
        self.log(f"Deposited £{amount}")
        self.record_transaction("[LOG] Deposit", amount)

    def withdraw(self, amount):
        super().withdraw(amount)
        self.log(f"Tried to withdraw £{amount}")
        self.record_transaction("[LOG] Withdraw", amount)