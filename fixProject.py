# SpiderRock Programming Assignment
# Matt Kusak
# m.kusak@wustl.edu

# Program reads FIX messages and:
# Lists error notifications for messages with same field twice
# Lists highest and lowest price of valid New Order Single messages by Account

# txt file -> array of fields
with open('Fix.Sample.txt') as file:
    data = file.read().split("|")

# last field of the message is tag 10
terminator = '10='

# array of fields -> message array (a.k.a. an array of arrays)
messages = []
current = []
for field in data:
    # cleans up data
    if field.startswith("\n"):
        field = field.replace("\n", "")
    current.append(field)
    if field.startswith(terminator):
        messages.append(current)
        current = []

# error notifications for repeating fields (set() uses hash table complexity)
# this implementation assumes error reporting for repeated FIELDS and not just TAGS.
# however, the code could be modified to filter the messages down to tags and check a similar way.
# another idea is to build a dictionary with keys = tags and values = FIX vals
n = 0
for message in messages:
    if len(message) != len(set(message)):
        print("\nDuplicate field error on message", n, ":", message)
    n += 1

# highest and lowest price of New Order Single messages by Account
new_order_single_identifier = '=D'
account_identifier = '1='
price_identifier = '44='

# simple loop to pull out messages matching '=D' tag
new_order_single_messages = []
for message in messages:
    nos_found = False
    for field in message:
        if field.endswith(new_order_single_identifier):
            nos_found = True
    if nos_found == True:
        new_order_single_messages.append(message)

# finds maximum and minimum prices of each account
# idea is to use a dictonary of arrays where keys = accounts and arrays = prices of new order single messages

accounts = []
for message in new_order_single_messages:
    for field in message:
        if field.startswith(account_identifier):
            current_account = field.replace(account_identifier, "")
            accounts.append(current_account)

# set() to remove duplicates
# creates dictionary with accounts as keys and empty arrays for prices
accounts = set(accounts)
message_dict = list(zip(accounts))
message_dict = {key: [] for key in accounts}

# input prices into arrays of corresponding accounts
for message in new_order_single_messages:
    # account tag comes before price tag, so this is valid for setting current account
    for field in message:
        if field.startswith(account_identifier):
            current_account = field.replace(account_identifier, "")
        if field.startswith(price_identifier):
            price = float(field.replace(price_identifier, ""))
            message_dict[current_account].append(price)

print("\n", message_dict)

for account in accounts:
    print("Account ", account, "has maximum NOS price: $", max(message_dict[account]), "and minimum NOS price: $", min(message_dict[account]))

# second part why are there multiple same prices