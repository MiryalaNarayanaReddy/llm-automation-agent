
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
    {
        "name": "count_week_days",
        "description":  "Count the number of occurrences of a specific weekday in the given file and write the result to an output file.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the file containing dates."
                },
                "day": {
                    "type": "string",
                    "description": "The name of the weekday to count. Must be one of Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday."
                },
                "output_path": {
                    "type": "string",
                    "description": "The path to the output file where the count will be written."
                }
            },
            "required": ["file_path", "day", "output_path"],
            "additionalProperties": False
        }
    },
    {
        "name": "sort_json_array",
        "description":  "Sorts an array of dictionaries in a JSON file by the specified keys and writes the result to an output file.",
        "parameters": {
            "type": "object",
            "properties": {
                "input_path": {
                    "type": "string",
                    "description": "The path to the input JSON file containing an array of objects."
                },
                "output_path": {
                    "type": "string",
                    "description": "The path to the output JSON file where the sorted data will be written."
                },
                "sort_keys": {
                    "type": "array",
                    "description": "A list of keys to sort by, in order of priority.",
                    "items": {
                        "type": "string",
                        "description": "A key to sort by."
                    }
                }
            },
            "required": ["input_path", "output_path", "sort_keys"],
            "additionalProperties": False
        }
    },

    {
        "name": "extract_recent_log_lines",
        "description":  "Extracts a specific line from the most recent `.log` files in a directory and writes them to an output file.",
        "parameters": {
            "type": "object",
            "properties": {
                "logs_directory": {
                    "type": "string",
                    "description": "The directory containing log files."
                },
                "output_path": {
                    "type": "string",
                    "description": "The path to the output file."
                },
                "num_files": {
                    "type": "integer",
                    "description": "The number of most recent log files to process (default: 10)."
                },
                "line_number": {
                    "type": "integer",
                    "description": "The line number to extract from each log file (default: 1)."
                }
            },
            "required": ["logs_directory", "output_path", "num_files", "line_number"],
            "additionalProperties": False
        }
    },
    {
        "name": "generate_markdown_index",
        "description":  "Finds all Markdown (`.md`) files in a directory and extracts the first occurrence of each H1. Creates an index file mapping filenames to their titles.",
        "parameters": {
            "type": "object",
            "properties": {
                "docs_directory": {
                    "type": "string",
                    "description": "The directory containing Markdown files."
                },
                "output_path": {
                    "type": "string",
                    "description": "The path to the output JSON file."
                }
            },
            "required": ["docs_directory", "output_path"],
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
    