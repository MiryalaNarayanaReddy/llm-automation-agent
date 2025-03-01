from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.responses import Response

from utils.model import LLMModel
from utils.tools import TOOLS
from utils.tools import PHASE_B_TOOLS


from utils.execute_tool import execute_all
from task_execute import execute_task

import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

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

llm.systemPrompt = '''
You are an automation agent. 
If there are any paths then make sure to return the same without changing or adding anything.
make sure to map the output of the commands to the corresponding function call.

'''

llm_for_phaseB = LLMModel("gpt-4o-mini", AIPROXY_TOKEN, PHASE_B_TOOLS)

llm_for_phaseB.systemPrompt = '''
You are an automation agent that executes tasks using Bash commands with cmd and Python scripts with code key.

Return commands and scripts without modification.
Maintain execution order, mixing Bash and Python where needed. (do not use bash command to install python packages inclue them in dependencies in code)
Python scripts are written to a file and executed using uv.
Map outputs to function calls.
if a library is inbuilt in the python code then do not include its installation in bash commands.
Raise error: path not allowed for paths outside /data.
do not include inbuilt libraries like sqlite3 or dateutil in dependencies list for uv but include them for python code
Use function tools for execution.
if any values are required like email or password then use placeholder random values like "john@gmail.com" or "password123"
'''

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
def run_task(task: str):
    try:
        result = llm.parseTask(task)
        function_call = result["choices"][0]["message"]["function_call"]

        if function_call:
            function_name = function_call["name"]
            arguments = function_call["arguments"]
            args = json.loads(arguments)
            if function_name == "phaseB_task":
                args['task'] = task
            status_code, details = execute_task(function_name, args, llm=llm, llm_for_phaseB=llm_for_phaseB)

            if status_code == 200:
                return JSONResponse(status_code=200, content={"message": details})
            else:
                raise HTTPException(status_code=status_code, detail=details)
        else:
            raise HTTPException(status_code=400, detail="Function call not found")

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error - " + str(e))

@app.get("/read")
def read_file_endpoint(path: str):
    try:
        with open(path, "r") as f:
            content = f.read()
        return Response(content, media_type="text/plain")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


import subprocess

# set git config
try: 
    subprocess.run(["git", "config", "--global", "user.email", "narayana@gmail.com"])
    subprocess.run(["git", "config", "--global", "user.name", "narayana"])
    print("Git config set successfully")
except subprocess.CalledProcessError as e:
    print(f"Error setting git config: {e}")

if __name__ == "__main__":
    import uvicorn  
    uvicorn.run(app, host="0.0.0.0", port=8000)
    # uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

