
TOOLS = [
    {
        "name": "data_generation_task",
        "description":  "Download datagen and generate data for project",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {    
                    "type": "string",
                    "description": "The url to download datagen and generate data for project"
                },
                "email": {
                    "type": "string",
                    "description": "The email to passed as argument to datagen.py"
                }
            },
            "required": ["url", "email"],
            "additionalProperties": False   
        }

    },
    {
        "name": "format_readme",
        "description":  "Formats the given file using the given prettier package.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The path to the file to format."
                },
                "prettier_package": {
                    "type": "string",
                    "description": "The name of the prettier package to use like prettier@3.4.2."
                }
            },
            "required": ["path", "prettier_package"],
            "additionalProperties": False
        }
    },
]

    # {
    #   "name": "execute_all",
    #   "description": "Executes a list of bash commands, Python code snippets, and Python scripts.",
    #   "parameters": {
    #     "type": "object",
    #     "properties": {
    #       "bash_commands": {
    #         "type": "array",
    #         "description": "List of bash commands to execute.",
    #         "items": {
    #           "type": "string",
    #           "description": "A bash command to execute."
    #         }
    #       },
    #       "python_codes": {
    #         "type": "array",
    #         "description": "List of Python code snippets to execute.",
    #         "items": {
    #           "type": "string",
    #           "description": "A Python code snippet to execute."
    #         }
    #       },
    #     },
    #     "required": ["bash_commands", "python_snippets", "python_scripts"],
    #     "additionalProperties": False
    #   }
    # }
    