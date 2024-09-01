import csv
from datetime import datetime, timedelta
import pytz

# Define the timezone
timezone = pytz.timezone('Asia/Kabul')  # Adjust this to your timezone

# Helper function to make datetime aware
def make_aware(datetime_str):
    naive_datetime = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
    return timezone.localize(naive_datetime).isoformat()

# Generate a list of 20 data entries
def generate_data(num_entries):
    base_date = datetime(2024, 9, 1, 9, 0, 0)
    data = []
    statuses = ["pending", "in_progress", "completed", "failed"]
    
    for i in range(1, num_entries + 1):
        scheduled_time = base_date + timedelta(days=i, hours=i % 24)
        status = statuses[i % len(statuses)]
        data.append({
            "user_id": (i % 2) + 1,  # Alternates between 1 and 2
            "name": f"Task {i}",
            "description": f"Task for testing - entry {i}",
            "price": 300 + i * 10.50,
            "scheduled_time": make_aware(scheduled_time.strftime('%Y-%m-%d %H:%M:%S')),
            "status": status,
            "result": "Completed successfully" if status == "completed" else "Work in progress",
            "created_at": make_aware(base_date.strftime('%Y-%m-%d %H:%M:%S')),
            "updated_at": make_aware(base_date.strftime('%Y-%m-%d %H:%M:%S')),
        })
    return data

# Generate 20 rows of data
data = generate_data(20)

# Open a new CSV file to write data
with open('job_data.csv', 'w', newline='') as csvfile:
    fieldnames = ["user_id", "name", "description", "price", "scheduled_time", "status", "result", "created_at", "updated_at"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write the header
    writer.writeheader()

    # Write the data rows
    for row in data:
        writer.writerow(row)

print("CSV data generated successfully.")
