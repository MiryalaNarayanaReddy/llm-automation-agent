import subprocess
import requests
import tempfile
from dateutil.parser import parse
import json
import os 
import sqlite3
import base64


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
            # print(f"Failed to download script, status code: {response.status_code}")
            return 400, f"Failed to download script, status code: {response.status_code}"

        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp_script:
            temp_script.write(response.content)
            temp_script_path = temp_script.name

        result = subprocess.run(["uv", "run", temp_script_path, f"{email}"], check=True)
        # return 200 if result.returncode == 0 else 400
        if result.returncode == 0:
            return 200, f"Executed script: {temp_script_path}"
        else:
            return 400, f"Failed to execute script, return code: {result.returncode}"
    except requests.RequestException as e:
        # print(f"Request error: {e}")
        return 400, f"Request error: {e}"
    except subprocess.CalledProcessError as e:
        # print(f"Execution error: {e}")
        return 400, f"Execution error: {e}"
    except Exception as e:
        # print(f"Unexpected error: {e}")
        return 400 , f"Unexpected error: {e}"

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
        # return 200 if result.returncode == 0 else 400
        if result.returncode == 0:
            return 200, f"Formatted file: {path}"
        else:  
            return 400, f"Failed to format file, return code: {result.returncode}"
    except subprocess.CalledProcessError as e:
        # print(f"Formatting error: {e}")
        return 400, f"Formatting error: {e}"

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
        # print(f"Invalid day: {day}")
        return 400, f"Invalid day: {day}"

    try:
        with open(file_path, "r") as f:
            dates = f.readlines()
        
        count = sum(1 for date in dates if parse(date.strip()).weekday() == week_day_map[day])
        
        with open(output_path, "w") as f:
            f.write(str(count))
        
        return 200, f"Count of {day} days: {count}"
    except Exception as e:
        # print(f"Error processing file: {e}")
        return 400, f"Error processing file: {e}"

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
            # print("Input JSON is not a list of objects.")
            return 400, f"Input JSON is not a list of objects."

        sorted_data = sorted(data, key=lambda x: tuple(x.get(key, "") for key in sort_keys))
        
        with open(output_path, "w") as f:
            json.dump(sorted_data, f, indent=4)
        
        return 200, f"Sorted JSON file: {output_path}"
    except Exception as e:
        # print(f"Error processing JSON file: {e}")
        return 400, f"Error processing JSON file: {e}"

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
        
        return 200, f"Extracted {len(recent_lines)} lines from {num_files} log files."
    except Exception as e:
        # print(f"Error processing log files: {e}")
        return 400, f"Error processing log files: {e}"

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
        
        return 200, f"Generated index: {output_path}"
    except Exception as e:
        # print(f"Error generating index: {e}")
        return 400, f"Error generating index: {e}"



def extract_email_sender(llm, system_message, input_path="/data/email.txt", output_path="/data/email-sender.txt"):
    try:
        with open(input_path, "r") as f:
            email_content = f.read()
        #   def getResponse(self, system_prompt, user_prompt, base64_image=None):

        response = llm.getResponse(system_message, email_content)
        email_sender = response["choices"][0]["message"]["content"].strip()
        with open(output_path, "w") as f:
            f.write(email_sender)
        
        return 200, f"Extracted email sender: {email_sender}"
    except Exception as e:
        # print(f"Error extracting email sender: {e}")
        return 400, f"Error extracting email sender: {e}"

def encode_image(image_path):
    """Encodes an image as Base64."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def extract_credit_card_number(llm, system_prompt, user_prompt, input_path="/data/credit-card.png", output_path="/data/credit-card.txt"):
    try:
        # Encode image to Base64
        base64_image = encode_image(input_path)

        # Send request to LLM
        response = llm.getResponse(
            system_prompt,
            user_prompt,
            base64_image=base64_image
        )

        # Extract and clean the credit card number
        card_number = response["choices"][0]["message"]["content"].replace(" ", "").strip()

        # Save extracted card number
        with open(output_path, "w") as f:
            f.write(card_number)
        
        return 200, f"Extracted credit card number: {card_number}"
    except Exception as e:
        # print(f"Error extracting credit card number: {e}")
        return 400, f"Error extracting credit card number: {e}"

def get_most_similar_comments(llm, input_path="/data/comments.txt", output_path="/data/comments-similar.txt", top_n=2):
   
    try: 
        with open(input_path, "r", encoding="utf-8") as f:
            data = [line.strip() for line in f.readlines() if line.strip()]

        top_n_similar_sentences = llm.getMostSimilarDocs( data, n=top_n)
    
        # write each value to a new line
        with open(output_path, "w", encoding="utf-8") as f:
            for doc in top_n_similar_sentences:
                f.write(f"{doc}\n")
            
        return 200, f"Extracted {len(top_n_similar_sentences)} most similar comments: {output_path}"
    
    except Exception as e:
        # print(f"Error extracting credit card number: {e}")
        return 400, f"Error extracting credit card number: {e}"

def total_gold_ticket_sales(db_path="/data/ticket-sales.db", output_path="/data/ticket-sales-gold.txt"):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT SUM(units * price) FROM tickets WHERE type = 'Gold'")
        total_sales = cursor.fetchone()[0] or 0
        conn.close()
        
        with open(output_path, "w") as f:
            f.write(str(total_sales))
        
        return 200, f"Calculated total sales of gold tickets: {total_sales}"
    except Exception as e:
        # print(f"Error calculating ticket sales: {e}")
        return 400, f"Error calculating ticket sales: {e}"
