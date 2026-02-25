
inventory = [
    {"item_id": 1, "name": "Espresso", "unit_price": 2.50, "stock": 40},
    {"item_id": 2, "name": "Latte", "unit_price": 4.25, "stock": 25},
    {"item_id": 3, "name": "Cold Brew", "unit_price": 3.75, "stock": 30},
    {"item_id": 4, "name": "Mocha", "unit_price": 4.50, "stock": 20},
    {"item_id": 5, "name": "Blueberry Muffin", "unit_price": 2.95, "stock": 18},
]


#- **Order 1:** Order iD: `"Order_101"`, Item ID: `2`, Quantity: `2`, Status: `"Placed"`, Total: `8.50`
#- **Order 2:** Order iD: `"Order_102"`, Item ID: `3`, Quantity: `1`, Status: `"Placed"`, Total: `3.75`


orders = [
    {
        "order_id": "order_101",
        "item_id" : 2,
        "quantity": 2,
        "status" : "placed",
        "total" : 8.50
    } ,
    {
        "order_id": "order_102",
        "item_id" : 3,
        "quantity": 1,
        "status" : "placed",
        "total" : 3.75
    }
]

#build key counter

next_id_number = 103


# Query 1: Place a new order for an item and quantity.


# 1. Input:
# ...
item_id = int(input("Enter the Item ID to order: "))
quantity = int(input("Enter the quantity: "))


# 2. Process: [Name process here, e.g. "Validate and create order"]
# ...
order_placed= False

for item in inventory:
    if item['item_id'] == item_id:
        if item['stock'] >= quantity:
            
            #generate key
            next_order_id = "order_" + str(next_id_number)
            next_id_number +=1
            

            total = quantity * item['unit_price'] 
            item['stock'] = item['stock'] - quantity
            

            #generate new order
            orders.append(
                            {
                    "order_id": next_order_id ,
                    "item_id" : item_id,
                    "quantity": quantity,
                    "status" : "placed",
                    "total" : total
                }
            )
            order_placed = True
            break


# 3. Output:
# ...
if order_placed: 
    print("Order Placed!")
else:
    print("Order could not be placed")

### Read

# Query 2: View all orders placed for a particular item.
# Prompt the user for the item name.

# 1. Input:
# ...
search_item = input("Enter the item name to search (e.g. 'Latte'): ")

# 2. Process: [Name process here, e.g. "Find orders for item"]
# ...

item_id = None
found = False

#find item id for an item name
for item in inventory:
    if item['name'] == search_item:
        item_id = item['item_id']
        found = True
        break


# find orders placed for an inventory item using item id. 
item_orders = []
if found:
    for order in orders:
        if order['item_id'] == item_id:
            item_orders.append(order)
            


# 3. Output:
# ...
if found:
    for order in item_orders:
        print(order)


# Query 3: Total number of orders placed for "Cold Brew".

# 1. Input:
# ...
item_name = "Cold Brew"



# 2. Process: [Name process here, e.g. "Count orders"]
# ...

# find item id for an item name
item_id = None
found = False
for item in inventory:
    if item['name'] == item_name:
        item_id = item['item_id']
        found = True
        break


#step 2: find how many orders placed for the item using item id
counter = 0
if found:
    for order in orders:
        if order['item_id'] == item_id:
            counter +=1



# 3. Output:
# ...
if found:
    print(f"Total number of orders for {item_name} is {counter}")
else:
    print("Not Found")


#Update
# Query 4: Update item stock quantity by item id.

# 1. Input:
# ...
item_id = int(input("Enter ID of item to update: "))
new_stock = int(input("Enter new stock quantity: "))

# 2. Process: [Name process here, e.g. "Validate and update stock"]
# ...


# update stock for an inventory item
counter = 0 
found = False
for item in inventory:
    if item['item_id'] == item_id:
        item['stock'] = new_stock
        found = True
        break



# 3. Output:
# ...
if found:
    print(f"Item quantity for item with item id = {item_id} is updated")
else:
    print("Not Found")

### Remove/Delete
# Query 5: Cancel an order and restore stock.

# 1. Input:
# ...
cancel_order_id = input("Enter Order ID to cancel: ")


# 2. Process: [Name process here, e.g. "Cancel order"]
# ...
found = False
for order in orders:
    if order['order_id'] == cancel_order_id:
        order['status'] = "cancelled"
        found = True
        item_id = order['item_id']
        quantity = order['quantity']


        #update inventory for an inventory item using item id
        for item in inventory:
            if item['item_id'] == item_id:
                item["stock"] = item["stock"] + quantity
                break

        break

# 3. Output:
# ...
if found:
    print(f"order was cancelled and inventory stock was updated")
else:
    print("Not Found")


## Check section (not included in the homework)
for item in inventory:
    print(item)

for order in orders:
    print(order)