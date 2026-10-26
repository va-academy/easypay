"""Estimate how long it may take to reach a savings goal."""

from decimal import Decimal, InvalidOperation, ROUND_CEILING


def read_money(prompt, allow_zero=False):
    """Read an INR amount with at most two decimal places."""
    while True:
        try:
            amount = Decimal(input(prompt).strip())
            if not amount.is_finite() or amount < 0 or (amount == 0 and not allow_zero):
                raise ValueError
            rounded = amount.quantize(Decimal("0.01"))
            if rounded != amount:
                raise ValueError
            return rounded
        except (InvalidOperation, ValueError):
            print("Enter a valid amount with at most two decimal places.")


def main():
    print("Savings Goal Planner")
    print("Use fictional amounts; this tool does not move or invest money.\n")

    goal = read_money("Savings goal (INR): ")
    saved = read_money("Amount already saved (INR): ", allow_zero=True)
    monthly_saving = read_money("Planned monthly saving (INR): ")

    remaining = max(goal - saved, Decimal("0.00"))
    if remaining == 0:
        print("You have already reached your savings goal.")
        return

    months = int((remaining / monthly_saving).to_integral_value(rounding=ROUND_CEILING))
    total_contributions = monthly_saving * months
    print(f"\nAmount remaining: INR {remaining:.2f}")
    print(f"Estimated time:   {months} month(s)")
    print(f"Total planned contributions: INR {total_contributions:.2f}")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")

# This loooks Good