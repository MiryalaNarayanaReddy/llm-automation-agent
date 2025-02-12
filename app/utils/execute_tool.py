import subprocess

def execute_bash_commands(commands: list[str]):
    """Execute a list of bash commands and handle errors."""
    for command in commands:
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Bash command failed: {command}\nError: {str(e)}")

def execute_python_code(code_snippets: list[str]):
    """Execute a list of Python code snippets and handle errors."""
    for code in code_snippets:
        try:
            exec(code)
        except Exception as e:
            raise RuntimeError(f"Python execution failed:\n{code}\nError: {str(e)}")

def execute_all(bash_commands: list[str], python_codes: list[str]):
    """Run bash commands first, then execute Python code and scripts, and verify success."""
    try:
        if bash_commands:
            execute_bash_commands(bash_commands)
        if python_codes:
            execute_python_code(python_codes)

        print("All commands executed successfully.")
    except RuntimeError as e:
        print(f"Execution failed:\n{e}")

# # Example usage:
# bash_cmds = ["echo 'Hello from Bash'", "ls"]
# python_snippets = ["print('Hello from Python')", "x = 42"]
# python_scripts = ["script1.py", "script2.py"]

# execute_all(bash_cmds, python_snippets, python_scripts)
