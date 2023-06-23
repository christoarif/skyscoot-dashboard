import csv
import random
from datetime import datetime, timedelta

# Define column names
columns = ["flightNumber", "departureTime", "OrderID", "ItemID", "ItemName", "UserID", "SeatNumber", "itemPrice", "quantity", "status", "orderTime", "itemWeight"]

# Specify the file path
csv_file_path = "mock_data.csv"

# Define the number of rows
num_rows = 3000

# Define the top item IDs for each flight number
flight_top_items = {
    "100": [1, 2, 3, 5],   # Flight 100 has top items with item IDs 1, 2, 3, 5
    "101": [1, 4, 5, 6],   # Flight 101 has top items with item IDs 1, 4, 5, 6
    "102": [2, 7, 8, 9],   # Flight 102 has top items with item IDs 2, 7, 8, 9
    "103": [2, 5, 10],     # Flight 103 has top items with item IDs 2, 5, 10
    "104": [3, 6, 8],      # Flight 104 has top items with item IDs 3, 6, 8
    "105": [1, 4, 7],      # Flight 105 has top items with item IDs 1, 4, 7
    "106": [9, 10],        # Flight 106 has top items with item IDs 9, 10
    "107": [2, 3],         # Flight 107 has top items with item IDs 2, 3
    "108": [4, 5, 8, 9],   # Flight 108 has top items with item IDs 4, 5, 8, 9
    "109": [6, 7],         # Flight 109 has top items with item IDs 6, 7
    "110": [8, 9, 10]      # Flight 110 has top items with item IDs 8, 9, 10
}

# Define the item lookup with item name, price, and weight
item_lookup = {
    1: ("Briyani", 0.5, 25.0),
    2: ("Nasi Lemak", 0.7, 15.0),
    3: ("Sandwich", 0.3, 12.0),
    4: ("Sushi", 0.2, 30.0),
    5: ("Dumplings", 0.4, 20.0),
    6: ("Coke", 0.1, 5.0),
    7: ("Beer", 0.3, 8.0),
    8: ("Plane Miniature", 0.8, 50.0),
    9: ("Perfume", 0.2, 80.0),
    10: ("Hoodie", 1.5, 70.0)
}

# Generate random sample data
data = []
flight_departure_times = {}

# Generate random departure times for each flight number
for i in range(num_rows):
    flight_number = str(random.randint(100, 110))
    if flight_number not in flight_departure_times:
        # Generate a list of 5 random departure times for each flight number
        departure_times = [datetime.now() - timedelta(days=random.randint(1, 7), hours=random.randint(0, 23), minutes=random.randint(0, 59)) for _ in range(5)]
        flight_departure_times[flight_number] = departure_times

    departure_time = random.choice(flight_departure_times[flight_number])
    order_id = i + 1  # Assign order ID as the index value

    if flight_number in flight_top_items and bool(random.getrandbits(1)):
        # Flight has top items, randomly select majority item ID from top items
        item_id = random.choice(flight_top_items[flight_number])
    else:
        # Flight does not have top items, generate random item ID
        item_id = random.randint(1, 10)

    item_name, item_weight, item_price = item_lookup[item_id]

    user_id = random.randint(1, 100)
    seat_number = random.choice(["A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3"])
    quantity = random.randint(1, 5)
    status = random.choice(["Out of Stock", "Success"])
    order_time = departure_time + timedelta(hours=random.randint(0, 12))

    data.append([
        flight_number,
        departure_time.strftime("%Y-%m-%d %H:%M:%S"),
        order_id,
        item_id,
        item_name,
        user_id,
        seat_number,
        item_price,
        quantity,
        status,
        order_time.strftime("%Y-%m-%d %H:%M:%S"),
        item_weight
    ])

# Write the data to the CSV file
with open(csv_file_path, "w", newline="") as file:
    writer = csv.writer(file)

    # Write the column names
    writer.writerow(columns)

    # Write the data rows
    writer.writerows(data)

print("Mock CSV file generated successfully.")
