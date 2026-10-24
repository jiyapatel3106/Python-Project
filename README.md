# 🏦 Bank Account Management System

A menu-driven, console-based banking application written in **Python**. It lets you create and manage Savings and Current accounts, move money between them, and keeps all data saved between runs.

This mini project demonstrates four core Python concepts: **Object-Oriented Programming (OOP)**, **Inheritance**, **File Handling**, and **Exception Handling**.
---

## ✨ Features

- Create **Savings** and **Current** accounts with an opening deposit
- **Deposit** and **withdraw** money
- **Check balance** and view full account details
- **Transfer money** between two accounts
- **Add interest** to Savings accounts
- View the **transaction history** of any account
- **List all accounts** at a glance
- **Delete** an account
- Data is **saved to a file** after every change, so nothing is lost when you exit

---

## 🧠 Concepts Demonstrated

| Concept | How it is used |
|---|---|
| **OOP** | Accounts and the bank are modelled as classes (`Bank`, `SavingsAccount`, etc.) with their own data and behaviour |
| **Inheritance** | Savings and Current accounts inherit shared behaviour (deposit, withdraw, history) from a common account class and add their own rules |
| **File Handling** | Account data is written to a file after each operation and loaded again on startup |
| **Exception Handling** | Custom exceptions such as `BankError` and `InvalidAmountError` handle bad input, missing accounts and invalid operations without crashing the program |

---

## 📋 Menu

```
===== BANK ACCOUNT MANAGEMENT SYSTEM =====
1. Create Account      5. Transfer Money
2. Deposit             6. Show Account Details
3. Withdraw            7. Add Interest (Savings)
4. Check Balance       8. Transaction History
9. List All Accounts   10. Delete Account
0. Exit
```

---
## 💡 Example Usage

```
Enter choice: 1
Type (Savings/Current): Savings
Account number: 1001
Holder name: Jiya Patel
Opening deposit: 5000
Created: <account details>

Enter choice: 2
Account number: 1001
Amount: 1500
Deposit successful. New balance: 6500.0
```

---

## 🛡️ Error Handling

The program handles problems gracefully and shows a clear message instead of crashing, for example:

- Entering text where a number is expected (`InvalidAmountError`)
- Trying to use an account number that does not exist
- Withdrawing or transferring more than the available balance
- Trying to add interest to a non-Savings account
- Entering an invalid menu choice

---
--# 📄 License

This project is for educational purposes. Add a license of your choice (for example MIT) before publishing.
