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


import requests
def query_llmfoundry(LLMFOUNDRY_TOKEN, user_input: str, tools: list):
    response = requests.post(
        "https://llmfoundry.straive.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {LLMFOUNDRY_TOKEN}:tds-course"},
        json={
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": user_input}],
            "functions": tools,
            "function_call": "auto"  # Let the model decide when to call a function
        }
    )
    return response.json()