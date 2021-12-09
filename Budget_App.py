class Category():
  def __init__(self, category):
    self.ledger = list()
    self.category = category

  def __str__(self):
    output = ""

    name_length = len(self.category)
    ast_left = (30 - name_length) / 2 if name_length % 2 == 0 else int((30 - name_length) / 2)
    ast_right = ast_left if name_length % 2 == 0 else ast_left + 1
    while ast_left > 0:
      output += "*"
      ast_left -= 1
    output += self.category
    while ast_right > 0:
      output += "*"
      ast_right -= 1

    for entry in self.ledger:
      amount = "{:.2f}".format(float(entry["amount"]))
      amount_len = len(amount)
      description_len = 23 if len(entry["description"]) > 23 else len(entry["description"])

      space = 30 - description_len - amount_len
      gap = ""
      if space > 0:
        while space > 0:
          gap += " "
          space -= 1

      output += "\n" + entry["description"][:23] + gap + amount

    output += "\n" + "Total: " + str("{:.2f}".format(float(self.get_balance())))
    return output

  def category_name(self):
    return self.category

  def deposit(self, amount, description = ""):
    self.ledger.append({"amount": amount, "description": description})
    return

  def withdraw(self, amount, description = ""):
    if not self.check_funds(amount):
      return False
    self.ledger.append({"amount": -amount, "description": description})
    return True

  def get_balance(self):
    balance = 0
    for entry in self.ledger:
      balance += entry["amount"]
    return balance

  def transfer(self, amount, category):
    if not self.check_funds(amount):
      return False
    self.withdraw(amount, "Transfer to " + category.category_name())
    category.deposit(amount, "Transfer from " + self.category_name())
    return True

  def check_funds(self, amount):
    if self.get_balance() < amount:
      return False
    return True

def create_spend_chart(categories):
  output = "Percentage spent by category\n"
  cat_len = len(categories)

  split = list()
  max_length = max(len(cat.category_name()) for cat in categories)

  # find amount spent in each category (absolute)
  spending = list()
  total_spent = 0
  for cat in categories:
    cat_spend = 0
    for amount in cat.ledger:
      if amount["amount"] < 0:
        cat_spend += abs(amount["amount"])
    spending.append(cat_spend)
    total_spent += cat_spend

    # for drawing x-axis
    word = list()
    for letter in cat.category_name():
      word.append(letter)
    spacing = max_length - len(cat.category_name())
    for i in range(spacing):
      word.append(" ")
    split.append(word)

  # find amount spent in each category (represented by number of "o")
  spending_perc = list()
  for spend in spending:
    spending_perc.append(int(spend / total_spent * 100 / 10))

  # draw "bar" chart
  def bar(spending_perc, y_axis, output):
    i = -1
    for spending in spending_perc:
      i += 1
      if spending * 10 == y_axis:
        output += "o  "
        spending_perc[i] -= 1
      else:
        output += "   "
    output += "\n"
    y_axis -= 10
    return [spending_perc, y_axis, output]

  y_axis = 100
  while y_axis >=0:
    if y_axis == 100:
      output += "100| "
      (spending_perc, y_axis, output) = bar(spending_perc, y_axis, output)
    if y_axis > 0:
      output += " " + str(y_axis) + "| "
      (spending_perc, y_axis, output) = bar(spending_perc, y_axis, output)
    if y_axis == 0:
      output += "  0| "
      (spending_perc, y_axis, output) = bar(spending_perc, y_axis, output)

  # draw dash
  output += "    -"
  for i in range(cat_len):
    output += "---"

  # draw x-axis
  format = list()
  for word in split:
    i = 0
    for letter in word:
      try:
        format[i].append(letter)
      except:
        format.append([letter])
      i += 1
  for line in format:
    output += "\n" + "     "
    for letter in line:
      output +=  letter + "  "

  return output
