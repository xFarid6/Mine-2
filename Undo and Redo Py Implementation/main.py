from banking.bank import Bank
from banking.controller import BankController
from banking.commands import Deposit, Withdrawal, Transfer, Batch


def main() -> None:

    # Create a bank
    bank = Bank()

    # create a bank controller
    controller = BankController()

    # create some accounts
    account1 = bank.create_account("ArjaCodes")
    account2 = bank.create_account("Goggles")
    account3 = bank.create_account("Gary")

    controller.execute(Deposit(account1, 100_000))

    controller.execute(Batch(
        commands = [
            Deposit(account2, 100_000),
            Deposit(account3, 100_000), 
            Transfer(from_account=account1, to_account=account2, amount=100_000)
        ]
    ))
    controller.undo()

    controller.execute(Deposit(account2, 100_000))
    controller.execute(Deposit(account3, 100_000))

    # transfer money
    controller.execute(
        Transfer(from_account=account2, to_account=account1, amount=100_000)
    )
    
    controller.execute(Withdrawal(account1, 100_000))
    controller.undo()

    print(bank)


if __name__ == "__main__":
    main()


""" First draft:

from banking.bank import Bank

def main() -> None:

    # Create a bank
    bank = Bank()

    # create some accounts
    account1 = bank.create_account("ArjaCodes")
    account2 = bank.create_account("Goggles")
    account3 = bank.create_account("Gary")

    account1.deposit(100_000)
    account2.deposit(100_000)
    account3.deposit(100_000)

    # transfer money
    account2.withdraw(50_000)
    account1.deposit(50_000)

    account1.withdraw(150_000)

    print(bank)


if __name__ == "__main__":
    main()
    
"""