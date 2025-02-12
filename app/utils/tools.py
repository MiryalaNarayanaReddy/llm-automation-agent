TOOLS = [
    {

        "name": "format_file",
        "description": "Format a file using the given requirements",
        "parameters": {
            "type": "object",
            "properties": {
                "install_command": {
                    "type": "string",
                    "description": "The command to install the required tools"
                },
                "execute_command": {
                    "type": "string",
                    "description": "The command to execute the formatting"
                }
            },
            "required": ["install_command", "execute_command"],
            "additionalProperties": False
        },
    },
]


