from fastapi import FastAPI
from fastapi.responses import JSONResponse
import os
import re
import requests
from fastapi.middleware.cors import CORSMiddleware
from utils.a1 import format_file
from utils.model import LLMModel
from utils.tools import TOOLS
from utils.execute_tool import execute_tool

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

@app.get("/")
async def root():
    """Return a welcome message"""  
    return {"message": "Welcome to the LLM Automation Agent!","token": AIPROXY_TOKEN}
@app.post("/run")
async def execute(task: str):
    """Execute a task and return 'done' if successful."""

    print(f"Executing task: {task}")
    response = llm.getResponse(task)

    # print(response.choices[0].message.function_call)
    function = response['choices'][0]['message']['function_call']

    if function is not None:
        function_name = function['name']
        arguments = json.loads(function['arguments'])

        res = {
            "function_name": function_name,
        }
        for key, value in arguments.items():
            res[key] = value
        
        execute_tool(function_name, arguments)
  
    return {}

@app.get("/read")
async def read(path: str):
    """Read a file and return its contents"""
    
    print(f"Reading file: {path}")

    # x = os.path.join(os.getcwd(),'./', path)

    # return {"content": open(x).read()}
    return {"content": path}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)