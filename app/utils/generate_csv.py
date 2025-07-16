from faker import Faker
import csv

fake = Faker()

with open('users.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    
    # Header
    writer.writerow(['firstName', 'lastName', 'email', 'phone'])
    
    # Generate 100 rows
    for _ in range(100):
        writer.writerow([
            fake.first_name(),
            fake.last_name(),
            fake.email(),
            fake.phone_number()
        ])

print("Generated users.csv with 100 records")
