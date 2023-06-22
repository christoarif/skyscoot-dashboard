import csv
import random
from datetime import datetime, timedelta

# Define column names
columns = ["flightNumber", "departureTime", "OrderID", "ItemID", "ItemName", "UserID", "SeatNumber", "itemPrice", "quantity", "status", "orderTime", "itemWeight"]

# Specify the file path
csv_file_path = "mock_data.csv"

# Define the number of rows
num_rows = 3000

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
    item_id = random.randint(1, 10)

    item_lookup = {
        1: ("Briyani", 0.5),
        2: ("Nasi Lemak", 0.7),
        3: ("Sandwich", 0.3),
        4: ("Sushi", 0.2),
        5: ("Dumplings", 0.4),
        6: ("Coke", 0.1),
        7: ("Beer", 0.3),
        8: ("Plane Miniature", 0.8),
        9: ("Perfume", 0.2),
        10: ("Hoodie", 1.5)
    }

    item_name, item_weight = item_lookup.get(item_id, ("Unknown", 0.0))

    user_id = random.randint(1, 100)
    seat_number = random.choice(["A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3"])
    item_price = round(random.uniform(10, 100), 2)
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
