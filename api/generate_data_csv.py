import csv
from datetime import datetime, timedelta

# Define the data you want to generate
def generate_data(num_entries):
    data = []
    tags_list = ['Programming', 'Development', 'Design', 'Management', 'Testing']
    statuses = ['pending', 'in_progress', 'completed', 'failed', 'canceled']
    
    for i in range(1, num_entries + 1):
        # Randomly select some tags
        selected_tags = [tags_list[j % len(tags_list)] for j in range(i % 3 + 1)]  # Select 1 to 3 tags
        tags = ', '.join(selected_tags)  # Convert list of tags to a comma-separated string

        data.append({
            "user_id": i % 3 + 1,  # Assuming 3 users for demo
            "name": f"Task {i}",
            "description": f"Description for task {i}",
            "price": round(300 + (i % 5) * 50, 2),
            "tags": tags,
            "scheduled_time": (datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d %H:%M:%S'),
            "status": statuses[i % 5],
            "result": "Work in progress" if statuses[i % 5] == 'in_progress' else "Completed" if statuses[i % 5] == 'completed' else "Failed" if statuses[i % 5] == 'failed' else "Pending",
            "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "updated_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    return data

# Save data to CSV
def save_to_csv(data):
    fieldnames = ["user_id", "name", "description", "price", "tags", "scheduled_time", "status", "result", "created_at", "updated_at"]
    with open('job_data.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write the header
        writer.writeheader()
        
        # Write the data rows
        for row in data:
            writer.writerow(row)

# Generate data and save to CSV
if __name__ == "__main__":
    print("Generating CSV data...")
    data = generate_data(20)
    save_to_csv(data)
    print("CSV data generated successfully.")
