import Budget_App
from Budget_App import create_spend_chart

# Example
food = Budget_App.Category("Food")
food.deposit(1000, "initial deposit")
food.withdraw(10.15, "groceries")
food.withdraw(15.89, "restaurant and more food for dessert")
print(food.get_balance())
clothing = Budget_App.Category("Clothing")
food.transfer(50, clothing)
clothing.withdraw(25.55)
clothing.withdraw(100)
auto = Budget_App.Category("Auto")
auto.deposit(1000, "initial deposit")
auto.withdraw(15)

print(create_spend_chart([food, clothing, auto]))
