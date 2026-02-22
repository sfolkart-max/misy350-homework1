inventory = [
    {"item_id": 1, "name": "Espresso", "unit_price": 2.50, "stock": 40},
    {"item_id": 2, "name": "Latte", "unit_price": 4.25, "stock": 25},
    {"item_id": 3, "name": "Cold Brew", "unit_price": 3.75, "stock": 30},
    {"item_id": 4, "name": "Mocha", "unit_price": 4.50, "stock": 20},
    {"item_id": 5, "name": "Blueberry Muffin", "unit_price": 2.95, "stock": 18},
]

'Order 1: Order iD: "Order_101", Item ID: 2, Quantity: 2, Status: "Placed", Total: 8.50'
'Order 2: Order iD: "Order_102", Item ID: 3, Quantity: 1, Status: "Placed", Total: 3.75'

# Query 0: View all items in the inventory with stock less than 20.

# 1. Input:
# Define the threshold for low stock (20) and access the inventory list.
threshold = 20

# 2. Process: Find items with stock below threshold
# Loop through the inventory to find matches
low_stock_items = []
for item in inventory:
    if item['stock'] < threshold:
        # Found one! Add it to our result list
        low_stock_items.append(item)

# 3. Output:
# Print the results
if len(low_stock_items) > 0:
    print('Low stock items found:')
    for item in low_stock_items:
        print(f'- {item["name"]}: {item["stock"]}')
else:
    print('No low stock items.')


    


# Query 1: Place a new order for an item and quantity.

# 1. Input
item_id = int(input('Enter the Item ID to order: '))
quantity = int(input('Enter the quantity: '))

# 2. Process: Validate and create order
selected_item = None

# Find the item
for item in inventory:
    if item['item_id'] == item_id:
        selected_item = item
        break

if selected_item is None:
    print('Item not found.')
else:
    if quantity <= 0:
        print('Invalid quantity.')
    elif selected_item['stock'] < quantity:
        print('Not enough stock available.')
    else:
        # Calculate total
        total = selected_item['unit_price'] * quantity
        
        # Update stock
        selected_item['stock'] -= quantity
        
        # Create order
        new_order = {
            "order_id": "Order_103",
            'item_id': item_id,
            'quantity': quantity,
            'status': 'Placed',
            'total': total
        }
        
        print('Order placed successfully!')
        print(f'Order Details: {new_order}')
        print(f'Updated stock for {selected_item["name"]}: {selected_item["stock"]}')




