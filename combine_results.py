import os
import json

# Input and output folder names
INPUT_FOLDER = "results"  # Assuming the previous script's output folder name
OUTPUT_FOLDER = "combined_results"

def combine_student_data(input_dir: str, output_dir: str):
    """
    Searches for student JSON files within semester ID folders in the input directory,
    combines the data for each student, and saves it to a new JSON file in the output directory.
    """
    os.makedirs(output_dir, exist_ok=True)
    student_data = {}

    # Iterate through all subdirectories (semester IDs) in the input folder
    for semester_id_dir in os.listdir(input_dir):
        semester_path = os.path.join(input_dir, semester_id_dir)
        if os.path.isdir(semester_path):
            print(f"Processing semester folder: {semester_id_dir}")
            # Iterate through all files in the semester folder
            for filename in os.listdir(semester_path):
                if filename.endswith(".json"):
                    student_id = filename[:-5]  # Remove ".json" extension
                    file_path = os.path.join(semester_path, filename)
                    try:
                        with open(file_path, 'r') as f:
                            data = json.load(f)
                            # Ensure the loaded data is a list
                            if isinstance(data, list):
                                if student_id not in student_data:
                                    student_data[student_id] = []
                                student_data[student_id].extend(data)
                            else:
                                print(f"Warning: Expected a list in {filename}, skipping its content.")
                    except FileNotFoundError:
                        print(f"Error: File not found: {file_path}")
                    except json.JSONDecodeError:
                        print(f"Error: Could not decode JSON in: {file_path}")

    # Save the combined data for each student
    for student_id, combined_data in student_data.items():
        output_filename = f"combined_{student_id}.json"
        output_path = os.path.join(output_dir, output_filename)
        try:
            with open(output_path, 'w') as outfile:
                json.dump(combined_data, outfile, indent=4)
            print(f"Combined data saved for student {student_id} in {output_filename}")
        except IOError:
            print(f"Error: Could not write to file: {output_path}")

if __name__ == "__main__":
    combine_student_data(INPUT_FOLDER, OUTPUT_FOLDER)
    print("\nCombining process completed.")
