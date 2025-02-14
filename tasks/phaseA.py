import subprocess
import requests
import tempfile
from dateutil.parser import parse
import json
import os 

def download_datagen(url, email):
    '''
    Download datagen script from URL and execute it with the given email.
    
    Args:
        url (str): The URL to download the datagen script.
        email (str): The email to pass as an argument to the script.
    
    Returns:    
        int: 200 if the execution was successful, 400 otherwise.
    '''
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to download script, status code: {response.status_code}")
            return 400

        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp_script:
            temp_script.write(response.content)
            temp_script_path = temp_script.name

        result = subprocess.run(["uv", "run", temp_script_path, f"email={email}"], check=True)
        return 200 if result.returncode == 0 else 400
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return 400
    except subprocess.CalledProcessError as e:
        print(f"Execution error: {e}")
        return 400
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 400

def format_readme(path, prettier_package="prettier@3.4.2"):
    '''
    Formats the given file using the specified Prettier package.

    Args:
        path (str): The path to the file to format.
        prettier_package (str): The Prettier package version (default: prettier@3.4.2).
    
    Returns:    
        int: 200 if the formatting was successful, 400 otherwise.
    '''
    try:
        result = subprocess.run(["npx", prettier_package, "--write", path], check=True)
        return 200 if result.returncode == 0 else 400
    except subprocess.CalledProcessError as e:
        print(f"Formatting error: {e}")
        return 400

def count_week_days(file_path, day, output_path):
    '''
    Count the number of occurrences of a specific weekday in the given file and write the result to an output file.

    Args:
        file_path (str): The path to the file containing dates.
        day (str): The name of the weekday to count.
        output_path (str): The path to the output file where the count will be written.

    Returns:    
        int: 200 if successful, 400 otherwise.
    '''
    week_day_map = {
        "Monday": 0,
        "Tuesday": 1,
        "Wednesday": 2,
        "Thursday": 3,
        "Friday": 4,
        "Saturday": 5,  
        "Sunday": 6
    }
    
    if day not in week_day_map:
        print(f"Invalid day: {day}")
        return 400

    try:
        with open(file_path, "r") as f:
            dates = f.readlines()
        
        count = sum(1 for date in dates if parse(date.strip()).weekday() == week_day_map[day])
        
        with open(output_path, "w") as f:
            f.write(str(count))
        
        return 200
    except Exception as e:
        print(f"Error processing file: {e}")
        return 400

def sort_json_array(input_path, output_path, sort_keys):
    '''
    Sorts an array of dictionaries in a JSON file by the specified keys and writes the result to an output file.

    Args:
        input_path (str): The path to the input JSON file containing an array of objects.
        output_path (str): The path to the output JSON file where the sorted data will be written.
        sort_keys (list): A list of keys to sort by, in order of priority.

    Returns:
        int: 200 if successful, 400 otherwise.
    '''
    try:
        with open(input_path, "r") as f:
            data = json.load(f)

        if not isinstance(data, list):
            print("Input JSON is not a list of objects.")
            return 400

        sorted_data = sorted(data, key=lambda x: tuple(x.get(key, "") for key in sort_keys))
        
        with open(output_path, "w") as f:
            json.dump(sorted_data, f, indent=4)
        
        return 200
    except Exception as e:
        print(f"Error processing JSON file: {e}")
        return 400

def extract_recent_log_lines(logs_directory, output_path, num_files=10, line_number=1):
    '''
    Extracts a specific line from the most recent `.log` files in a directory and writes them to an output file.

    Args:
        logs_directory (str): The directory containing log files.
        output_path (str): The path to the output file.
        num_files (int): The number of most recent log files to process (default: 10).
        line_number (int): The line number to extract from each log file (default: 1).

    Returns:
        int: 200 if successful, 400 otherwise.
    '''
    try:
        log_files = [
            (os.path.getmtime(os.path.join(logs_directory, f)), f)
            for f in os.listdir(logs_directory) if f.endswith(".log")
        ]
        
        log_files.sort(reverse=True, key=lambda x: x[0])
        
        recent_lines = []
        for _, log_file in log_files[:num_files]:
            with open(os.path.join(logs_directory, log_file), "r") as f:
                lines = f.readlines()
                if len(lines) >= line_number:
                    recent_lines.append(lines[line_number - 1].strip())
                else:
                    recent_lines.append("")  # Append empty string if line_number is out of range
        
        with open(output_path, "w") as f:
            f.write("\n".join(recent_lines) + "\n")
        
        return 200
    except Exception as e:
        print(f"Error processing log files: {e}")
        return 400


def generate_markdown_index(docs_directory, output_path):
    '''
    Finds all Markdown (`.md`) files in a directory and extracts the first occurrence of each H1.
    Creates an index file mapping filenames (relative to docs_directory) to their titles.

    Args:
        docs_directory (str): The directory containing Markdown files.
        output_path (str): The path to the output JSON file.

    Returns:
        int: 200 if successful, 400 otherwise.
    '''
    try:
        index = {}
        docs_directory = os.path.abspath(docs_directory)
        
        for root, _, files in os.walk(docs_directory):
            for file in files:
                if file.endswith(".md"):
                    file_path = os.path.abspath(os.path.join(root, file))
                    rel_path = os.path.relpath(file_path, docs_directory)
                    
                    with open(file_path, "r", encoding="utf-8") as f:
                        for line in f:
                            if line.startswith("# "):
                                index[rel_path] = line[2:].strip()
                                break
        
        output_path = os.path.abspath(output_path)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(index, f, indent=4)
        
        return 200
    except Exception as e:
        print(f"Error generating index: {e}")
        return 400