import json
from datetime import datetime, timedelta
from collections import defaultdict
import os

# Loading JSON data from the file taking the file name as input.
def load_data(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

#COunting people that completed each training
def count_completed_trainings(data):
    training_count = defaultdict(set)
    for person in data:
        for completion in person['completions']:
            training_count[completion['name']].add(person['name'])
    
    ççç
    training_count = {training: len(people) for training, people in training_count.items()}
    return training_count

# Listing individuals who are completing specific training programs during the current fiscal year.
def completed_trainings_in_fiscal_year(data, trainings, fiscal_year):
    fiscal_start = datetime(fiscal_year - 1, 7, 1)
    fiscal_end = datetime(fiscal_year, 6, 30)
    
    completed_in_fy = defaultdict(list)
    
    for person in data:
        for completion in person['completions']:
            completion_date = datetime.strptime(completion['timestamp'], '%m/%d/%Y')
            if completion['name'] in trainings and fiscal_start <= completion_date <= fiscal_end:
                completed_in_fy[completion['name']].append(person['name'])
    
    return completed_in_fy

# Identify individuals whose training has expired or is about to expire soon.
def find_expired_or_expiring_trainings(data, reference_date):
    reference_date = datetime.strptime(reference_date, '%Y-%m-%d')
    soon_threshold = reference_date + timedelta(days=30)
    
    expired_or_expiring = defaultdict(list)
    
    for person in data:
        for completion in person['completions']:
            if completion['expires']:
                expiration_date = datetime.strptime(completion['expires'], '%m/%d/%Y')
                if expiration_date < reference_date:
                    expired_or_expiring[person['name']].append({
                        'training': completion['name'],
                        'status': 'expired',
                        'expiration_date': completion['expires']
                    })
                elif reference_date <= expiration_date <= soon_threshold:
                    expired_or_expiring[person['name']].append({
                        'training': completion['name'],
                        'status': 'expires soon',
                        'expiration_date': completion['expires']
                    })
    
    return expired_or_expiring

# Saving the output to JSON file
def save_to_json(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

# Console options for user's entry
def console_menu():
    print("===== Training Data Processing Application =====")
    print("Please choose an option:")
    print("1. Upload data file")
    print("2. Count people who completed each training")
    print("3. List people who completed specific trainings in Fiscal Year 2024")
    print("4. Find expired or expiring trainings (as of October 1, 2023)")
    print("5. Exit")
    print("===============================================")

def run_application():
    data = None

    while True:
        console_menu()
        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            # Prompting user for JSON file path
            file_path = input("Please provide the path to the JSON data file: ").strip()
            if os.path.exists(file_path):
                try:
                    data = load_data(file_path)
                    print("Data file successfully loaded.")
                except Exception as e:
                    print(f"Error loading file: {e}")
            else:
                print("File not found. Please try again.")

        elif choice == '2':
            # Counting people that completed training
            if data:
                training_count = count_completed_trainings(data)
                save_to_json(training_count, 'output_training_count.json')
                print("Training count saved to 'output_training_count.json'.")
            else:
                print("No data loaded. Please upload the data file first (Option 1).")

        elif choice == '3':
            # Completed trainings in fiscal year 2024
            if data:
                trainings_list = ["Electrical Safety for Labs", "X-Ray Safety", "Laboratory Safety Training"]
                completed_fy2024 = completed_trainings_in_fiscal_year(data, trainings_list, 2024)
                save_to_json(completed_fy2024, 'output_completed_fy2024.json')
                print("Fiscal Year 2024 training completions saved to 'output_completed_fy2024.json'.")
            else:
                print("No data loaded. Please upload the data file first (Option 1).")

        elif choice == '4':
            # Finding expired or expiring trainings
            if data:
                expired_or_expiring = find_expired_or_expiring_trainings(data, '2023-10-01')
                save_to_json(expired_or_expiring, 'output_expired_or_expiring.json')
                print("Expired or expiring trainings saved to 'output_expired_or_expiring.json'.")
            else:
                print("No data loaded. Please upload the data file first (Option 1).")

        elif choice == '5':
            # Exit the application
            print("Exiting the application. Goodbye!")
            break

        else:
            print("Invalid choice, please try again.")

if __name__ == '__main__':
    run_application()
