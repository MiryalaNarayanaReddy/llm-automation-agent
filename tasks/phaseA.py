import subprocess
import requests
import tempfile

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
