from fastapi import FastAPI
from fastapi.responses import JSONResponse
import os
import re
import requests
from fastapi.middleware.cors import CORSMiddleware
from utils.tools import query_llmfoundry, TOOLS
from utils.a1 import format_file

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


import json

@app.get("/")
async def root():
    """Return a welcome message"""  
    return {"message": "Welcome to the LLM Automation Agent!","token": AIPROXY_TOKEN}
@app.post("/run")
async def execute(task: str):
    """Execute a task and return 'done' if successful."""

    print(f"Executing task: {task}")
    response = query_llmfoundry(AIPROXY_TOKEN, task, TOOLS)

    # Extract function call details
    choices = response.get("result", {}).get("choices", [])
    
    if not choices:
        return {"error": "No function call detected."}

    function_call = choices[0].get("message", {}).get("function_call", {})

    if not function_call:
        return {"error": "No valid function call found."}

    function_name = function_call.get("name")
    arguments = json.loads(function_call.get("arguments", "{}"))

    if function_name == "format_file":
        try:
            format_file(arguments["install_command"], arguments["execute_command"])
            return {"result": "done"}
        except Exception as e:
            return {"error": str(e)}

    return {"error": "Function not supported."}

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