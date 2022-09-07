from dataclasses import dataclass, field
from banking.account import Account
from banking.transaction import Transaction


@dataclass
class Deposit:
    account: Account
    amount: int

    @property
    def transaction_details(self) -> str: 
        return f"${self.amount / 100:.2f} to account {self.account.name}"


    def execute(self) -> None:
        self.account.deposit(self.amount)
        print(f"Deposited {self.transaction_details}")


    def undo(self) -> None:
        self.account.withdraw(self.amount)
        print(f"Undoed {self.transaction_details}")


    def redo(self) -> None:
        self.account.deposit(self.amount)
        print(f"Redid deposited {self.transaction_details}")


@dataclass
class Withdrawal:
    account: Account
    amount: int

    @property
    def transaction_details(self) -> str: 
        return f"${self.amount / 100:.2f} to account {self.account.name}"


    def execute(self) -> None:
        self.account.withdraw(self.amount)
        print(f"Withdrawn {self.transaction_details}")

    
    def undo(self) -> None:
        self.account.deposit(self.amount)
        print(f"Undoed withdrawal {self.transaction_details}")


    def redo(self) -> None:
        self.account.withdraw(self.amount)
        print(f"Redid withdrawal {self.transaction_details}")


@dataclass
class Transfer:
    from_account: Account
    to_account: Account
    amount: int


    @property
    def transfer_details(self) -> str:
        return f"{self.amount/100:.2f} from account {self.from_account} to {self.to_account}"


    def execute(self) -> None:
        self.from_account.withdraw(self.amount)
        self.to_account.deposit(self.amount)
        print(f"Transferred {self.transfer_details}")


    def undo(self) -> None:
        self.to_account.withdraw(self.amount)
        self.from_account.deposit(self.amount)
        print(f"Undid transfer of {self.transfer_details}")


    def redo(self) -> None:
        self.from_account.withdraw(self.amount)
        self.to_account.deposit(self.amount)
        print(f"Redid transfer of {self.transfer_details}")


@dataclass
class Batch:
    commands: list[Transaction] = field(default_factory=list)

    def execute(self) -> None:
        completed_commands: list[Transaction] = []
        try:
            for command in self.commands:
                command.execute()
                completed_commands.append(command)
        except ValueError as e:
            print(f"Command error: {e}")
            for command in reversed(completed_commands):
                command.undo()

    
    def undo(self) -> None:
        for command in reversed(self.commands):
            command.undo()

    
    def redo(self) -> None:
        for command in self.commands:
            command.redo()