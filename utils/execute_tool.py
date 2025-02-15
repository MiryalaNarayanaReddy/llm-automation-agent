import subprocess
import json

def execute_bash_command(command: str):
    """Execute a bash command and capture its output."""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        return {"type": "bash_commands", "output": result.stdout.strip() or "Success"}
    except subprocess.CalledProcessError as e:
        return {"type": "bash_commands", "output": f"Error: {e.stderr.strip()}"}

def execute_python_code(python_code: str, filename: str = "temp_script.py"):
    """Write Python code to a file and execute it using uv."""
    with open(filename, "w") as f:
        f.write(python_code)

    try:
        result = subprocess.run(["uv", "run", filename], check=True, capture_output=True, text=True)
        return {"type": "python_code", "output": result.stdout.strip() or "Success"}
    except subprocess.CalledProcessError as e:
        return {"type": "python_code", "output": f"Error: {e.stderr.strip()}"}

def execute_all(commands: list[dict]):
    """Execute a mix of Bash commands and Python code sequentially, capturing results."""
    results = []

    # print(commands)

    try :
        for command in commands:
            if command["type"] == "bash_commands":
                results.append(execute_bash_command(command["cmd"]))
            elif command["type"] == "python_code":
                results.append(execute_python_code(command["code"]))
            elif command["type"] == "python_script":
                results.append(execute_python_code(command["code"]))  # Same execution method for scripts

        return 200, results
    except Exception as e:
        return 400, f"Error executing commands: {e}"

# Example usage
llm_response = [
    {"type": "bash_commands", "cmd": "echo 'Hello from Bash'"},
    {"type": "python_code", "code": "print('Hello from Python')"},
    {"type": "python_script", "code": "import sys\nprint(f'Python version: {sys.version}')"}
]

result_json = execute_all(llm_response)
print(result_json)