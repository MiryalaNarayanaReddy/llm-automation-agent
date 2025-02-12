
TOOLS = [
    {
      "name": "execute_all",
      "description": "Executes a list of bash commands, Python code snippets, and Python scripts.",
      "parameters": {
        "type": "object",
        "properties": {
          "bash_commands": {
            "type": "array",
            "description": "List of bash commands to execute.",
            "items": {
              "type": "string",
              "description": "A bash command to execute."
            }
          },
          "python_snippets": {
            "type": "array",
            "description": "List of Python code snippets to execute.",
            "items": {
              "type": "string",
              "description": "A Python code snippet to execute."
            }
          },
          "python_scripts": {
            "type": "array",
            "description": "List of Python script file paths to execute.",
            "items": {
              "type": "string",
              "description": "A Python script file path."
            }
          }
        },
        "required": ["bash_commands", "python_snippets", "python_scripts"],
        "additionalProperties": False
      }
    }
]

