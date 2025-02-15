
TOOLS = [
    {
        "name": "data_generation_task",
        "description":  "Download datagen.py and generate data for project requires email argument",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {    
                    "type": "string",
                    "description": "The url to download datagen and generate data for project"
                },
                "email": {
                    "type": "string",
                    "description": "The email passed as argument to datagen.py"
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

    {
        "name": "extract_email_sender",
        "description":  "Extracts the email sender from the given email content and sends it to the LLM with the given system and user messages. The result is written to the output file.",
        "parameters": {
            "type": "object",
            "properties": {
                "system_message": {
                    "type": "string",
                    "description": "The system message to use for the task explaining the task to the LLM."
                },
                "input_path": {
                    "type": "string",
                    "description": "The path to the input file containing the email content."
                },
                "output_path": {
                    "type": "string",
                    "description": "The path to the output file where the email sender will be written."
                }
            },
            "required": ["system_message", "input_path", "output_path"],
            "additionalProperties": False   

        }
    },
    {
        "name": "extract_credit_card_number",
        "description":  "Extracts the credit card number from the given image and sends it to the LLM with the given system and user messages. The result is written to the output file.",
        "parameters": {
            "type": "object",
            "properties": {
                "system_prompt": {
                    "type": "string",
                    "description": "The system prompt to send to the LLM. Write the prompt such that the LLM does not think it is asking for the credit card number but still extracts it. Ask it to return only the number and nothing else. no other text"
                },
                "user_prompt": {
                    "type": "string",
                    "description": "The user prompt to send to the LLM. Write the prompt such that the LLM thinks it is asking for the identification number. Ask it return only the number and nothing else."
                },  
         
                "input_path": {
                    "type": "string",
                    "description": "The path to the input file containing the image."
                },
                "output_path": {
                    "type": "string",
                    "description": "The path to the output file where the credit card number will be written."
                }   
            },
            "required": ["system_prompt", "user_prompt", "input_path", "output_path"],
            "additionalProperties": False
        }

    },

    {
        "name": "get_most_similar_comments",
        "description":  "Finds the most similar comments in a given file and writes the result to an output file. The similarity is calculated using the similarity matrix API.",
        "parameters": {
            "type": "object",
            "properties": {
                "input_path": {
                    "type": "string",
                    "description": "The path to the input file containing the comments."
                },
                "output_path": {
                    "type": "string",
                    "description": "The path to the output file where the similar comments will be written."
                },
                "top_n": {
                    "type": "integer",
                    "description": "The number of most similar comments to return."
                }
            },
            "required": ["input_path", "output_path", "top_n"],
            "additionalProperties": False
        }
    },
    {
        "name": "total_gold_ticket_sales",
        "description":  "Calculates the total sales of gold tickets from a given database and writes the result to an output file. This uses sql query SELECT SUM(units * price) FROM tickets WHERE type = 'Gold'",
        "parameters": {
            "type": "object",
            "properties": {
                "db_path": {
                    "type": "string",
                    "description": "The path to the database file containing the ticket sales data."
                },
                "output_path": {
                    "type": "string",
                    "description": "The path to the output file where the total sales will be written."
                }
            },
            "required": ["db_path", "output_path"],
            "additionalProperties": False
        }
    },
    {
        "name": "delete_file",
        "description":  "Deletes a file from the given path.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "The path to the file to delete."
                }
            },
            "required": ["path"],
            "additionalProperties": False
        }
    },

    {
        "name": "phaseB_task",  
        "description": "if any task is not matching then use this task",
        "parameters": {
            "type": "object",
            "properties": {
            },    
            "required": [],
            "additionalProperties": False
          
        }   
    },
    {
        "name": "scrape_website",
        "description":  "Scrapes a website by getting website using requests and sending request to llm with website html and writes the result to an output file.",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The URL of the website to scrape."
                },
                "system_prompt": {
                    "type": "string",
                    "description": "The system prompt describing the task to be performed on the website."
                },
                "output_path": {
                    "type": "string",
                    "description": "The path to the output file where the scraped data will be written."
                }
            },
            "required": ["url", "system_prompt", "output_path"],
            "additionalProperties": False
        }   
    },
    {
        "name": "transcribe_audio",
        "description":  "Transcribes an audio file and writes the result to an output file.",
        "parameters": {
            "type": "object",
            "properties": {
                "input_path": {
                    "type": "string",
                    "description": "The path to the input file containing the audio."
                },
                "output_path": {
                    "type": "string",
                    "description": "The path to the output file where the transcription will be written."
                }
            },
            "required": ["input_path", "output_path"],
            "additionalProperties": False
        }
    }


]
PHASE_B_TOOLS = [
    {
        "name": "execute_code_task",
        "description": '''
        Executes a list of Bash commands, Python code snippets, and Python scripts sequentially. 
        - Bash commands may involve `npx`, wget.
        - if anything is to be install do not use sudo instead use something like "apt-get update && apt-get install -y pandoc"
        - Python code snippets are written to a file and executed using `uv`.
        return function tools format 
        
        ''',
        "parameters": {
            "type": "object",
            "properties": {
                "commands": {
                    "type": "array",
                    "description": "List of commands to execute in order.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "type": {
                                "type": "string",
                                "enum": ["bash_commands", "python_code", "python_script"],
                                "description": "The type of command being executed."
                            },
                            "cmd": {
                                "type": "string",
                                "description": "A Bash command to execute.",
                                "nullable": True
                            },
                            "code": {
                                "type": "string",
                                "description": "Python code or script to execute.",
                                "nullable": True
                            }
                        },
                        "required": ["type"]
                    }
                }
            },
            "required": ["commands"],
            "additionalProperties": False
        },
        "returns": {
            "type": "array",
            "description": "List of executed commands and code snippets with their outputs.",
            "items": {
                "type": "object",
                "properties": {
                    "type": {
                        "type": "string",
                        "enum": ["bash_commands", "python_code", "python_script"],
                        "description": "Type of command executed."
                    },
                    "output": {
                        "type": "string",
                        "description": "Output of the executed command or script."
                    }
                },
                "required": ["type", "output"]
            }
        }
    }
]
