import os
import json
import requests
import time

# Base URL and parameters
BASE_URL = "http://peoplepulse.diu.edu.bd:8189/result"
SEMESTER_ID_START = "202"
SEMESTER_ID_END = "251"
STUDENT_ID_START = 652
STUDENT_ID_END = 652
STUDENT_ID_PREFIX = "202-35-"
OUTPUT_FOLDER_PREFIX = "results"
OTHER_STUDENTS = [
]
OUTPUT_STUDENT_LIST_FILE = "student_ids.json"

def is_valid_semester_id(semester_id: str) -> bool:
    """Checks if a semester ID is in the valid format."""
    if len(semester_id) != 3 or not semester_id[:2].isdigit() or semester_id[2] not in ('1', '2', '3'):
        return False
    return True

def fetch_result(semester_id: str, student_id: str):
    """Fetches result data for a given semester ID and student ID."""
    params = {
        'semesterId': semester_id,
        'studentId': student_id
    }
    retries = 3
    while retries > 0:
        try:
            response = requests.get(BASE_URL, params=params)
            if response.status_code == 200:
                data = response.json()
                if not data:  # Empty array, no retries
                    print(f"Empty data returned for student {student_id} in semester {semester_id}, skipping retries.")
                    return None
                return data
            else:
                print(f"Failed to fetch data for student {student_id} in semester {semester_id}, Status Code: {response.status_code}")
                break
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for student {student_id} in semester {semester_id}: {e}")
            retries -= 1
            if retries > 0:
                print(f"Retrying in 3 seconds... ({retries} retries left)")
                time.sleep(3)
            else:
                print(f"Failed to fetch data for student {student_id} in semester {semester_id} after multiple retries.")
        return None

def save_json(output_folder: str, student_id: str, data: dict):
    """Saves the fetched data to a JSON file."""
    file_path = os.path.join(output_folder, f"{student_id}.json")
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    print(f"Data saved for student {student_id} in {output_folder}")

def generate_semester_ids(start_id: str, end_id: str) -> list[str]:
    """Generates a list of semester IDs within the given range."""
    semester_ids = []
    start_year = int(start_id[:2])
    start_semester = int(start_id[2])
    end_year = int(end_id[:2])
    end_semester = int(end_id[2])

    for year in range(start_year, end_year + 1):
        start_sem = 1 if year > start_year else start_semester
        end_sem = 3 if year < end_year else end_semester
        for semester in range(start_sem, end_sem + 1):
            semester_ids.append(f"{year:02d}{semester}")
    return semester_ids

def generate_student_ids(start: int, end: int, prefix: str, others: list[str]) -> list[str]:
    """Generates a sorted list of student IDs."""
    students = set(others)
    for i in range(start, end + 1):
        students.add(f"{prefix}{i}")
    return sorted(list(students))

def save_student_ids(student_ids: list[str], output_file: str):
    """Saves the list of student IDs to a JSON file."""
    with open(output_file, 'w') as f:
        json.dump(student_ids, f, indent=4)
    print(f"List of student IDs saved to {output_file}")

def main():
    semester_ids = generate_semester_ids(SEMESTER_ID_START, SEMESTER_ID_END)
    student_ids = generate_student_ids(STUDENT_ID_START, STUDENT_ID_END, STUDENT_ID_PREFIX, OTHER_STUDENTS)
    # save_student_ids(student_ids, OUTPUT_STUDENT_LIST_FILE)
    print("Fetching data for students:", student_ids)
    print("Fetching data for semesters:", semester_ids)
    print()

    for semester_id in semester_ids:
        print()
        if not is_valid_semester_id(semester_id):
            print(f"Invalid semester ID: {semester_id}. Skipping.")
            continue

        output_folder = os.path.join(OUTPUT_FOLDER_PREFIX, semester_id)
        os.makedirs(output_folder, exist_ok=True)

        for student_id in student_ids:
            print()
            file_path = os.path.join(output_folder, f"{student_id}.json")
            if os.path.exists(file_path):
                print(f"File already exists for student {student_id} in semester {semester_id}, skipping.")
                continue

            print(f"Fetching data for student {student_id} in semester {semester_id}...")
            data = fetch_result(semester_id, student_id)
            if data:
                save_json(output_folder, student_id, data)
            else:
                print(f"No valid data for student {student_id} in semester {semester_id}")

if __name__ == '__main__':
    main()
