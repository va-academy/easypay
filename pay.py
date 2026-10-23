"""EasyPay: a practice finance tracker using fictional transactions only."""

import json
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path


DATA_FILE = Path(__file__).with_name("transactions.json")


def load_transactions():
    """Read saved transactions, or start with an empty ledger."""
    if not DATA_FILE.exists():
        return []
    with DATA_FILE.open(encoding="utf-8") as file:
        transactions = json.load(file)
    if not isinstance(transactions, list):
        raise ValueError("Saved transactions must be a list.")
    for entry in transactions:
        if entry["type"] not in ("income", "expense"):
            raise ValueError("Unknown transaction type.")
        amount = Decimal(entry["amount"])
        if not amount.is_finite() or amount <= 0:
            raise ValueError("Invalid saved amount.")
        if not isinstance(entry["description"], str):
            raise ValueError("Invalid saved description.")
        datetime.fromisoformat(entry["date"])
    return transactions


def read_amount():
    """Use Decimal so money calculations avoid floating-point rounding."""
    while True:
        try:
            amount = Decimal(input("Amount (INR): ").strip())
            if not amount.is_finite() or amount <= 0:
                raise ValueError
            rounded = amount.quantize(Decimal("0.01"))
            if rounded != amount:
                raise ValueError
            return rounded
        except (InvalidOperation, ValueError):
            print("Enter a positive amount with at most two decimal places.")


def add_transaction(transactions, transaction_type):
    amount = read_amount()
    description = input("Description: ").strip() or "General"
    entry = {
        "date": datetime.now().isoformat(timespec="seconds"),
        "type": transaction_type,
        "amount": str(amount),
        "description": description,
    }
    updated = transactions + [entry]
    # Replace the saved file only after the new contents have been written.
    temporary_file = DATA_FILE.with_suffix(".tmp")
    temporary_file.write_text(json.dumps(updated, indent=2), encoding="utf-8")
    temporary_file.replace(DATA_FILE)
    transactions.append(entry)
    print(f"Saved {transaction_type}: INR {amount:.2f}")


def show_summary(transactions):
    income = sum(
        (Decimal(item["amount"]) for item in transactions if item["type"] == "income"),
        Decimal("0.00"),
    )
    expenses = sum(
        (Decimal(item["amount"]) for item in transactions if item["type"] == "expense"),
        Decimal("0.00"),
    )
    print(f"\nTotal income:   INR {income:.2f}")
    print(f"Total expenses: INR {expenses:.2f}")
    print(f"Balance:        INR {income - expenses:.2f}")


def show_history(transactions):
    if not transactions:
        print("No transactions yet. Add some sample income or expenses!")
        return
    print("\nDate                Type       Amount (INR)  Description")
    print("-" * 65)
    for item in transactions:
        print(
            f"{item['date'].replace('T', ' ')} "
            f"{item['type']:<8} {Decimal(item['amount']):>12.2f}  "
            f"{item['description']}"
        )


def main():
    print("Welcome to EasyPay — a sample finance tracker")
    print("Practice with fictional data. This app does not move real money.")
    try:
        transactions = load_transactions()
    except (OSError, ValueError, KeyError, TypeError, InvalidOperation) as error:
        print(f"Could not load {DATA_FILE.name}: {error}")
        print("Fix or rename that file before restarting. Your data was not changed.")
        return

    while True:
        print("\n1. Add income\n2. Add expense\n3. View balance\n4. View history\n5. Exit")
        choice = input("Choose an option: ").strip()
        if choice in ("1", "2"):
            try:
                add_transaction(transactions, "income" if choice == "1" else "expense")
            except OSError as error:
                print(f"Could not save transaction: {error}")
        elif choice == "3":
            show_summary(transactions)
        elif choice == "4":
            show_history(transactions)
        elif choice == "5":
            print("Thanks for using EasyPay!")
            break
        else:
            print("Please choose a number from 1 to 5.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")
