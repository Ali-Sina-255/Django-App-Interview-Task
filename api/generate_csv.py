import csv
from datetime import datetime
import pytz

# Define the timezone
timezone = pytz.timezone('Asia/Kabul')  # Adjust this to your timezone

# Helper function to make datetime aware
def make_aware(datetime_str):
    naive_datetime = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
    return timezone.localize(naive_datetime).isoformat()

# Define the data you want to generate
data = [
    {"user_id": 1, "name": "Python", "description": "Task for testing Python skills", "price": 300.00, "scheduled_time": make_aware("2024-09-05 10:30:00"), "status": "pending", "result": "Work in progress", "created_at": make_aware("2024-09-01 09:00:00"), "updated_at": make_aware("2024-09-01 09:00:00")},
    {"user_id": 1, "name": "Django", "description": "Task for testing Django skills", "price": 350.50, "scheduled_time": make_aware("2024-09-06 10:30:00"), "status": "in_progress", "result": "Work in progress", "created_at": make_aware("2024-09-01 09:00:00"), "updated_at": make_aware("2024-09-01 09:00:00")},
    {"user_id": 1, "name": "React", "description": "Task for testing React skills", "price": 400.00, "scheduled_time": make_aware("2024-09-07 10:30:00"), "status": "completed", "result": "Completed successfully", "created_at": make_aware("2024-09-01 09:00:00"), "updated_at": make_aware("2024-09-01 09:00:00")},
    {"user_id": 2, "name": "JavaScript", "description": "Task for JavaScript development", "price": 320.00, "scheduled_time": make_aware("2024-09-08 11:00:00"), "status": "failed", "result": "Failed due to error", "created_at": make_aware("2024-09-01 09:00:00"), "updated_at": make_aware("2024-09-01 09:00:00")},
    {"user_id": 2, "name": "HTML", "description": "Task for HTML page creation", "price": 280.00, "scheduled_time": make_aware("2024-09-09 09:00:00"), "status": "in_progress", "result": "Ongoing work", "created_at": make_aware("2024-09-01 09:00:00"), "updated_at": make_aware("2024-09-01 09:00:00")},
]

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
