import os
import json

# Input and output folder names
INPUT_FOLDER = "combined_results"
OUTPUT_FOLDER = "students-info"

def calculate_cgpa(data: list[dict]) -> float:
    """Calculates CGPA from a list of course data, considering highest points for repeated courses."""
    course_records = {}
    for item in data:
        course_id = item.get('customCourseId')
        points = item.get('pointEquivalent')
        if course_id is not None and points is not None:
            points = float(points)
            if course_id not in course_records or points > course_records[course_id]['pointEquivalent']:
                course_records[course_id] = {'pointEquivalent': points, 'totalCredit': float(item.get('totalCredit', 0))}

    total_weighted_points = 0
    total_credits = 0
    for record in course_records.values():
        total_weighted_points += record['totalCredit'] * record['pointEquivalent']
        total_credits += record['totalCredit']

    if total_credits > 0:
        return total_weighted_points / total_credits
    return 0.0

def process_combined_results(input_dir: str, output_dir: str):
    """
    Processes each combined student result file, calculates CGPA,
    and saves student ID and CGPA to a single JSON file.
    """
    os.makedirs(output_dir, exist_ok=True)
    student_cgpas = []

    for filename in os.listdir(input_dir):
        if filename.startswith("combined_") and filename.endswith(".json"):
            student_id = filename[len("combined_"):-5]
            file_path = os.path.join(input_dir, filename)
            try:
                with open(file_path, 'r') as f:
                    combined_data = json.load(f)
                    if isinstance(combined_data, list):
                        cgpa = calculate_cgpa(combined_data)
                        student_cgpas.append({"student_id": student_id, "cgpa": round(cgpa, 3)})
                    else:
                        print(f"Warning: Expected a list in {filename}, skipping CGPA calculation.")
            except FileNotFoundError:
                print(f"Error: File not found: {file_path}")
            except json.JSONDecodeError:
                print(f"Error: Could not decode JSON in: {file_path}")

    # Save the array of student IDs and CGPAs to a single JSON file
    output_file_path = os.path.join(output_dir, "student_cgpas.json")
    try:
        with open(output_file_path, 'w') as outfile:
            json.dump(student_cgpas, outfile, indent=4)
        print(f"\nStudent IDs and CGPAs saved to {output_file_path}")
    except IOError:
        print(f"Error: Could not write to file: {output_file_path}")

if __name__ == "__main__":
    process_combined_results(INPUT_FOLDER, OUTPUT_FOLDER)
    print("\nCGPA calculation and saving process completed.")