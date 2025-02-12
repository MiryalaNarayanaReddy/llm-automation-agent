from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils.model import LLMModel
from utils.tools import TOOLS
from utils.execute_tool import execute_all
import os

AIPROXY_TOKEN = os.environ.get("AIPROXY_TOKEN")

if not AIPROXY_TOKEN:
    raise ValueError("AIPROXY_TOKEN is not set. Please set it as an environment variable.")

print(f"Using AI Proxy Token: {AIPROXY_TOKEN[:5]}*****")  # Masked for security

# Initialize FastAPI app
app = FastAPI()

# Configure CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change this for security)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


# configure model

llm = LLMModel("gpt-4o-mini", AIPROXY_TOKEN, TOOLS)

import json

'''

{
  "arguments": {
    "bash_commands": ["echo 'Running Prettier'", "npx prettier --write /data/format.md"],
    "python_snippets": ["print('Processing Python...')", "x = 42"],
    "python_scripts": ["/data/script1.py", "/data/script2.py"]
  },
  "function_name": "execute_all"
}
execute_all(bash_commands, python_snippets, python_scripts)
'''


@app.get("/")
async def root():
    """Return a welcome message"""  
    return {"message": "Welcome to the LLM Automation Agent!","token": AIPROXY_TOKEN}


@app.post("/run")
async def execute(task: str):
    """Execute a task and return 'done' if successful."""

    print(f"Executing task: {task}")
    response = llm.getResponse(task)
    print(response)
    # print(response.choices[0].message.function_call)
    function = response["choices"][0]["message"]["function_call"]

    if function is not None:
        function_name = function['name']
        arguments = json.loads(function['arguments'])

        # return {"arguments": arguments, "function_name": function_name}
    
        
        bash_commands = []
        python_snippets =[]  
        python_scripts = []
        if "bash_commands" in arguments:
            bash_commands = arguments["bash_commands"]
        if "python_snippets" in arguments:
            python_snippets = arguments["python_snippets"]
        if "python_scripts" in arguments:   
            python_scripts = arguments["python_scripts"]

        print(f"Executing function: {function_name}")
        print(f"Bash commands: {bash_commands}")
        print(f"Python snippets: {python_snippets}")    
        print(f"Python scripts: {python_scripts}")

        try: 
            execute_all(bash_commands, python_snippets, python_scripts)
        except Exception as e:
            return {"error": str(e)}    
    else:
        return {"error": "No function call found in the response"}


@app.get("/read")
async def read(path: str):
    """Read a file and return its contents"""
    
    print(f"Reading file: {path}")

    # x = os.path.join(os.getcwd(),'./', path)

    # return {"content": open(x).read()}
    return {"content": path}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)