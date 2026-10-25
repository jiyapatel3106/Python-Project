"""
Bank Account Management System
Concepts: OOP, Inheritance, File Handling (JSON), Exception Handling
"""

import json
import os
from datetime import datetime

DATA_FILE = "bank_data.json"


# ---------- Custom Exceptions ----------
class BankError(Exception):
    """Base class for all bank-related errors."""


class InvalidAmountError(BankError):
    pass


class InsufficientFundsError(BankError):
    pass


class AccountNotFoundError(BankError):
    pass


class DuplicateAccountError(BankError):
    pass


# ---------- Base Class ----------
class Account:
    account_type = "Basic"

    def __init__(self, acc_no, name, balance=0.0, history=None):
        self.acc_no = acc_no
        self.name = name
        self._balance = balance          # protected attribute (encapsulation)
        self.history = history or []

    @property
    def balance(self):
        return self._balance

    def _log(self, text):
        self.history.append(f"{datetime.now():%Y-%m-%d %H:%M} | {text}")

    def deposit(self, amount):
        if amount <= 0:
            raise InvalidAmountError("Deposit amount must be greater than 0.")
        self._balance += amount
        self._log(f"Deposited {amount:.2f}")

    def withdraw(self, amount):
        if amount <= 0:
            raise InvalidAmountError("Withdrawal amount must be greater than 0.")
        if amount > self._balance:
            raise InsufficientFundsError("Insufficient balance.")
        self._balance -= amount
        self._log(f"Withdrew {amount:.2f}")

    def to_dict(self):
        return {"type": self.account_type, "acc_no": self.acc_no,
                "name": self.name, "balance": self._balance,
                "history": self.history}

    def __str__(self):
        return (f"[{self.account_type}] A/C {self.acc_no} | {self.name} | "
                f"Balance: Rs. {self._balance:.2f}")


# ---------- Derived Classes (Inheritance) ----------
class SavingsAccount(Account):
    account_type = "Savings"
    MIN_BALANCE = 500
    INTEREST_RATE = 0.04                 # 4% per year

    def withdraw(self, amount):          # method overriding
        if amount > 0 and self._balance - amount < self.MIN_BALANCE:
            raise InsufficientFundsError(
                f"Savings account must keep minimum Rs. {self.MIN_BALANCE}.")
        super().withdraw(amount)

    def add_interest(self):
        interest = self._balance * self.INTEREST_RATE
        self._balance += interest
        self._log(f"Interest added {interest:.2f}")
        return interest


class CurrentAccount(Account):
    account_type = "Current"
    OVERDRAFT_LIMIT = 5000

    def withdraw(self, amount):          # method overriding
        if amount <= 0:
            raise InvalidAmountError("Withdrawal amount must be greater than 0.")
        if amount > self._balance + self.OVERDRAFT_LIMIT:
            raise InsufficientFundsError("Overdraft limit exceeded.")
        self._balance -= amount
        self._log(f"Withdrew {amount:.2f}")


ACCOUNT_TYPES = {"Savings": SavingsAccount, "Current": CurrentAccount}


# ---------- Bank (manages accounts + file handling) ----------
class Bank:
    def __init__(self, filename=DATA_FILE):
        self.filename = filename
        self.accounts = {}
        self.load()

    def load(self):
        if not os.path.exists(self.filename):
            return
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
            for d in data:
                cls = ACCOUNT_TYPES[d["type"]]
                self.accounts[d["acc_no"]] = cls(
                    d["acc_no"], d["name"], d["balance"], d["history"])
        except (json.JSONDecodeError, KeyError):
            print("Warning: data file is corrupted. Starting with empty bank.")
        except OSError as e:
            print("File error:", e)

    def save(self):
        try:
            with open(self.filename, "w") as f:
                json.dump([a.to_dict() for a in self.accounts.values()], f, indent=4)
        except OSError as e:
            print("Could not save data:", e)

    def get(self, acc_no):
        if acc_no not in self.accounts:
            raise AccountNotFoundError(f"Account {acc_no} not found.")
        return self.accounts[acc_no]

    def create_account(self, acc_type, acc_no, name, opening=0.0):
        if acc_no in self.accounts:
            raise DuplicateAccountError("Account number already exists.")
        if acc_type not in ACCOUNT_TYPES:
            raise BankError("Invalid account type.")
        acc = ACCOUNT_TYPES[acc_type](acc_no, name)
        if opening:
            acc.deposit(opening)
        self.accounts[acc_no] = acc
        self.save()
        return acc

    def transfer(self, from_no, to_no, amount):
        src, dst = self.get(from_no), self.get(to_no)
        src.withdraw(amount)
        dst.deposit(amount)
        self.save()

    def delete_account(self, acc_no):
        self.get(acc_no)
        del self.accounts[acc_no]
        self.save()


# ---------- Menu-driven program ----------
def read_amount(prompt):
    try:
        return float(input(prompt))
    except ValueError:
        raise InvalidAmountError("Please enter a valid number.")


def main():
    bank = Bank()
    menu = """
===== BANK ACCOUNT MANAGEMENT SYSTEM =====
1. Create Account      5. Transfer Money
2. Deposit             6. Show Account Details
3. Withdraw            7. Add Interest (Savings)
4. Check Balance       8. Transaction History
9. List All Accounts   10. Delete Account
0. Exit
"""
    while True:
        print(menu)
        choice = input("Enter choice: ").strip()
        try:
            if choice == "1":
                t = input("Type (Savings/Current): ").strip().capitalize()
                no = input("Account number: ").strip()
                name = input("Holder name: ").strip()
                amt = read_amount("Opening deposit: ")
                print("Created:", bank.create_account(t, no, name, amt))
            elif choice == "2":
                acc = bank.get(input("Account number: ").strip())
                acc.deposit(read_amount("Amount: "))
                bank.save()
                print("Deposit successful. New balance:", acc.balance)
            elif choice == "3":
                acc = bank.get(input("Account number: ").strip())
                acc.withdraw(read_amount("Amount: "))
                bank.save()
                print("Withdrawal successful. New balance:", acc.balance)
            elif choice == "4":
                print("Balance:", bank.get(input("Account number: ").strip()).balance)
            elif choice == "5":
                a = input("From account: ").strip()
                b = input("To account: ").strip()
                bank.transfer(a, b, read_amount("Amount: "))
                print("Transfer successful.")
            elif choice == "6":
                print(bank.get(input("Account number: ").strip()))
            elif choice == "7":
                acc = bank.get(input("Account number: ").strip())
                if not isinstance(acc, SavingsAccount):
                    raise BankError("Interest applies to Savings accounts only.")
                print(f"Interest added: {acc.add_interest():.2f}")
                bank.save()
            elif choice == "8":
                acc = bank.get(input("Account number: ").strip())
                print("\n".join(acc.history) or "No transactions yet.")
            elif choice == "9":
                for a in bank.accounts.values():
                    print(a)
                if not bank.accounts:
                    print("No accounts yet.")
            elif choice == "10":
                bank.delete_account(input("Account number: ").strip())
                print("Account deleted.")
            elif choice == "0":
                print("Thank you for banking with us!")
                break
            else:
                print("Invalid choice. Try again.")
        except BankError as e:               # our custom exceptions
            print("Error:", e)
        except Exception as e:               # anything unexpected
            print("Unexpected error:", e)


if __name__ == "__main__":
    main()
