from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException

from utils.model import LLMModel
from utils.tools import TOOLS

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
        # result = execute_task(task)
        result = llm.parseTask(task)

        function_call = result["choices"][0]["message"]["function_call"]

        if function_call:

            function_name = function_call["name"]
            arguments = function_call["arguments"]
            args = json.loads(arguments)  
            status_code, details = execute_task(function_name, args, llm=llm)
        return {"status_code": status_code, "details": details}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/read")
def read_file_endpoint(path: str):
    with open(path, "r") as f:
        content = f.read()
    if content is None:
        raise HTTPException(status_code=404, detail="File not found")
    return content


if __name__ == "__main__":
    import uvicorn  
    uvicorn.run(app, host="0.0.0.0", port=8000)
    # uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)


# cat ./data/dates.txt | while read date; do if [[ $(date -d "$date" +%A) == "Wednesday" ]]; then echo "$date"; fi done | wc -l > ./data/dates-wednesdays.txt
