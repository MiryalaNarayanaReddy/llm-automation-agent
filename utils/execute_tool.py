import subprocess
import json
import time


def execute_bash_command(command: str):
    """Execute a bash command and capture its output."""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        return {"type": "bash_commands", "output": result.stdout.strip() or "Success", "success": True}
    except subprocess.CalledProcessError as e:
        return {"type": "bash_commands", "output": f"Error: {e.stderr.strip()}", "success": False}

def execute_python_code(python_code: str, filename: str = "./temp_script.py"):
    """Write Python code to a file and execute it using uv."""
    with open(filename, "w") as f:
        f.write(python_code)

    try:
        result = subprocess.run(["uv", "run", filename], check=True, capture_output=True, text=True)
        return {"type": "python_code", "output": result.stdout.strip() or "Success", "success": True}
    except subprocess.CalledProcessError as e:
        return {"type": "python_code", "output": f"Error: {e.stderr.strip()}", "success": False}

def request_fix_from_llm(llm_for_phaseB, error_message: str, command: str, max_retries=3):
    """Request a fix from the LLM when a command fails."""
    print(f"Requesting fix from LLM for error: {error_message}")
    
    prompt = f'''
    Write bash commands to fix the error 
    rerun the comand that failed.
    make sure to use the same command as the original command 
    ```
    {command}
    ```
    do not change the command. or add a new command that is not in the original command.
If needed, use placeholder values. "
    "For example: git config --global user.email 'your-email' -> "
    "git config --global user.email 'john@gmail.com'
              
              '''
    
    llm_response = llm_for_phaseB.fix_request(prompt, error_message, command)
    function_call = llm_response.get("choices", [{}])[0].get("message", {}).get("function_call")
    
    if function_call:
        function_name = function_call.get("name")
        if function_name == "execute_code_task":
            arguments = json.loads(function_call.get("arguments", "{}"))  
            
            if "commands" in arguments:
                status_code, details = execute_all(llm_for_phaseB, arguments['commands'], max_retries=max_retries-1)
                return status_code, details
            else:
                return 400, "No commands returned from LLM"
        else:
            return 400, f"Function not found: {function_name}"
    else:
        return 400, "Function call not found"

def execute_all(llm_for_phaseB, commands: list[dict], max_retries=3):
    """Execute a mix of Bash commands and Python code, retrying failed commands."""
    
    if max_retries < 1:
        return 400, "Max retries exceeded"
    
    results = []
    all_success = True
    
    for command in commands:
        retries = 0
        print("Executing command:", command)
        
        while retries < max_retries:
            if command["type"] == "bash_commands":
                result = execute_bash_command(command["cmd"])
            elif command["type"] in ["python_code", "python_script"]:
                result = execute_python_code(command["code"])
            else:
                result = {"success": False, "output": "Unknown command type"}
            
            if result["success"]:
                results.append({"type": command["type"], "output": result["output"], "success": True})
                break  # Move to the next command if successful
            else:
                print(f"Attempt {retries + 1} failed: {result['output']}")
                comd = command["cmd"] if command["type"] == "bash_commands" else command["code"]
                code, detail = request_fix_from_llm(llm_for_phaseB, result['output'], comd, max_retries=max_retries-1)

                if code == 200:
                    break  # Move to the next command if successful
                else:
                    results.append({"type": command["type"], "output": f"Final Failure: {detail}", "success": False})
                    all_success = False
                    break  # Stop retrying if the fix request failed
            
            retries += 1
        
        if retries == max_retries and not result["success"]:
            results.append({"type": command["type"], "output": f"Final Failure: {result['output']}", "success": False})
            all_success = False
    
    return (200 if all_success else 400), results
