class BankAccount:      
    def __init__(self, balance):
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            return True                                        #return True if the withdrawal was successful
        else:
            return False                                       #return False if the withdrawal failed
         
    def get_balance(self):
        return self.balance


account = BankAccount(1000)

result1 = account.withdraw(300)
print(f'Withdraw 300: {result1}, New Balance: {account.get_balance()}')             #returns True, New Balance: 700

result2 = account.withdraw(5000)
print(f'Withdraw 5000: {result2}, insufficient funds: {account.get_balance()}')     #returns False, insufficient funds: 700


-----------output-----------
"""
Withdraw 300: True, New Balance: 700
Withdraw 5000: False, insufficient funds: 700
"""