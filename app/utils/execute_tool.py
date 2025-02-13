import subprocess

def execute_bash_commands(commands: list[str]):
    """Execute a list of bash commands and handle errors."""
    for command in commands:
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Bash command failed: {command}\nError: {str(e)}")
        
def execute_python_code_from_file(python_code: list[str], filename: str = "temp_script.py"):
    """Write Python code to a file and execute it."""
    with open(filename, "w") as f:
        f.write("\n".join(python_code))

    try:
        import subprocess
        subprocess.run(["python", filename], check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Python execution failed with error:\n{e}")


def execute_all(bash_commands: list[str], python_codes: list[str]):
    """Run bash commands first, then execute Python code and scripts, and verify success."""
    try:
        if bash_commands:
            execute_bash_commands(bash_commands)
        if python_codes:
            execute_python_code_from_file(python_codes)

        print("All commands executed successfully.")
    except RuntimeError as e:
        print(f"Execution failed:\n{e}")
