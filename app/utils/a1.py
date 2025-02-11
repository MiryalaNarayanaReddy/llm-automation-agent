import subprocess
def execute_OS_command(command: str):
    """Execute a shell command and handle errors."""
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Command failed: {command}\nError: {str(e)}")

def format_file(install_command: str, execute_command: str):
    """Run the install command first, then execute the formatting command."""
    execute_OS_command(install_command)
    execute_OS_command(execute_command)

# format_file("npm install -g prettier@3.4.2","prettier --write ./data/format.md")