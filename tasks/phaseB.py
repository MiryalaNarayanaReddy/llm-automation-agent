import os


def checkIsSafe(filepath: str) -> bool:
    abs_path = os.path.abspath(filepath)
    data_dir = os.path.abspath("/data")

    if abs_path.startswith(data_dir):
        return True
    else:
        return False


def deleteFile(filepath: str) -> bool:
    
    # removing is not allowed forbidden status code 403
    return 403, f"Removing {filepath} is not allowed"


# def fetchDataAndSave(url: str, output_path: str) -> bool:
#     try:
#         response = requests.get(url,verify=False)
#         if response.status_code != 200:
#             print(f"Failed to fetch data from {url}, status code: {response.status_code}")
#             return 400, f"Failed to fetch data from {url}, status code: {response.status_code}"

#         with open(output_path, "wb") as f:
#             f.write(response.content)
        
#         return 200
#     except requests.RequestException as e:
#         print(f"Request error: {e}")
#         return 400, f"Request error: {e}"
#     except Exception as e:
#         print(f"Unexpected error: {e}")
#         return 400, f"Unexpected error: {e}"


# # B4. Clone a git repo and make a commit

# def cloneRepoAndCommit(repo_url: str, commit_message: str, output_path: str) -> bool:
#     try:
#         # Run git clone command
#         result = subprocess.run(["git", "clone", repo_url, output_path], check=True)

#         # Change directory to the cloned repo
#         os.chdir(output_path)

#         # Run git commit command
#         result = subprocess.run(["git", "commit", "-m", commit_message], check=True)

#         return 200

#     except subprocess.CalledProcessError as e:
#         print(f"Git command error: {e}")
#         return 400, f"Git command error: {e}"

#     except Exception as e:
#         print(f"Unexpected error: {e}")
#         return 400, f"Unexpected error: {e}"
    

# # B5. Run a SQL query on a SQLite or DuckDB database

# def runSqlQuery(db_path: str, query: str) -> bool:
#     try:
#         # Connect to the database
#         conn = sqlite3.connect(db_path)
#         cursor = conn.cursor()

#         # Execute the query
#         cursor.execute(query)

#         # Fetch the results
#         results = cursor.fetchall()

#         # Print the results
#         for row in results:
#             print(row)

#         # Close the database connection
#         conn.close()

#         return 200
#     except sqlite3.Error as e:
#         print(f"SQLite error: {e}")
#         return 400, f"SQLite error: {e}"
#     except Exception as e:
#         print(f"Unexpected error: {e}")    
#         return 400, f"Unexpected error: {e}"
    

# B6. Extract data from (i.e. scrape) a website
# B7. Compress or resize an image

# B8. Transcribe audio from an MP3 file

# B9. Convert Markdown to HTML

# B10. Write an API endpoint that filters a CSV file and returns JSON data
