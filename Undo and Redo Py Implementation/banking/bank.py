from dataclasses import dataclass, field
import random
import string

from banking.account import Account


@dataclass
class Bank:
    accounts: dict[str, Account] = field(default_factory=dict)

    def create_account(self, name: str) -> Account:
        number = "".join(random.choices(string.digits, k=12))
        account = Account(name=name, number=number, balance=0)
        self.accounts[number] = account
        return account


    def get_account(self, account_number: str) -> Account:
        return self.accounts[account_number]
