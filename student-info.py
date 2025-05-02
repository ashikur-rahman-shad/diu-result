import os
import json
import requests
import time

# Base URL
BASE_URL = "http://peoplepulse.diu.edu.bd:8189/result/studentInfo"

# Student ID parameters
STUDENT_ID_START = 720
STUDENT_ID_END = 751
STUDENT_ID_PREFIX = "212-35-"
OTHER_STUDENTS = [
    "211-35-713",
    "211-35-720",
    "212-35-3178",
    "212-35-3179",
    "212-35-3180",
    "212-35-3181",
    "212-35-3183",
    "212-35-3182",
    "202-35-3114"
]
OUTPUT_FILE = "students-info/students-info.json"

def generate_student_ids(start: int, end: int, prefix: str, others: list[str]) -> list[str]:
    """Generates a sorted list of student IDs."""
    students = set(others)
    for i in range(start, end + 1):
        students.add(f"{prefix}{i}")
    return sorted(list(students))

def fetch_student_info(student_id: str) -> dict or None:
    """Fetches student information for a given student ID."""
    params = {
        'studentId': student_id
    }
    retries = 3
    while retries > 0:
        try:
            response = requests.get(BASE_URL, params=params)
            if response.status_code == 200:
                data = response.json()
                return data  # Return the data if successful
            else:
                print(f"Failed to fetch student info for {student_id}. Status code: {response.status_code}")
                break # Exit loop on non-200
        except requests.exceptions.RequestException as e:
            print(f"Error fetching student info for {student_id}: {e}")
            retries -= 1
            if retries > 0:
                print(f"Retrying in 3 seconds... ({retries} retries left)")
                time.sleep(3)
            else:
                print(f"Failed to fetch student info for {student_id} after multiple retries.")
        return None  # Return None on exception or non-200 status after retries

def save_student_info(data: list[dict], filename: str):
    """Saves the combined student information to a JSON file."""
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Student information saved to {filename}")
    except IOError as e:
        print(f"Error saving student information to {filename}: {e}")

def main():
    """Main function to fetch and save student information."""
    student_ids = generate_student_ids(STUDENT_ID_START, STUDENT_ID_END, STUDENT_ID_PREFIX, OTHER_STUDENTS)
    print("Fetching student info for IDs:", student_ids)

    all_student_info = []
    for student_id in student_ids:
        info = fetch_student_info(student_id)
        if info:
            all_student_info.append(info)  # Append the fetched data to the list
        else:
            print(f"Skipping saving info for {student_id} as no data was retrieved.")

    if all_student_info:
        save_student_info(all_student_info, OUTPUT_FILE)
    else:
        print("No student information was successfully fetched.  No file will be saved.")

if __name__ == "__main__":
    main()
