from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils.model import LLMModel
from utils.tools import TOOLS
from utils.execute_tool import execute_all
import os
from fastapi import FastAPI, HTTPException
# from agent.file_manager import read_file
from task_execute import execute_task
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
        result = llm.getResponse(task)

        function_call = result["choices"][0]["message"]["function_call"]

        if function_call:
            print("function_call", function_call)
            function_name = function_call["name"]
            arguments = function_call["arguments"]
            execute_task(function_name, arguments)



        return {"status": "success", "output": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")



# {
#   "status": "success",
#   "output": {
#     "id": "chatcmpl-B0ppJqHxmYmsCG5EI2prpHlYlwRDZ",
#     "object": "chat.completion",
#     "created": 1739538921,
#     "model": "gpt-4o-mini-2024-07-18",
#     "choices": [
#       {
#         "index": 0,
#         "message": {
#           "role": "assistant",
#           "content": null,
#           "function_call": {
#             "name": "format_readme",
#             "arguments": "{\"path\":\"./data/format.md\",\"prettier_package\":\"prettier@3.4.2\"}"
#           },
#           "refusal": null
#         },
#         "logprobs": null,
#         "finish_reason": "function_call"
#       }
#     ],
#     "usage": {
#       "prompt_tokens": 291,
#       "completion_tokens": 35,
#       "total_tokens": 326,
#       "prompt_tokens_details": {
#         "cached_tokens": 0,
#         "audio_tokens": 0
#       },
#       "completion_tokens_details": {
#         "reasoning_tokens": 0,
#         "audio_tokens": 0,
#         "accepted_prediction_tokens": 0,
#         "rejected_prediction_tokens": 0
#       }
#     },
#     "service_tier": "default",
#     "system_fingerprint": "fp_00428b782a",
#     "monthlyCost": 0.014232000000000002,
#     "cost": 0.001083,
#     "monthlyRequests": 35
#   }
# }

@app.get("/read")
def read_file_endpoint(path: str):
    content = read_file(path)
    if content is None:
        raise HTTPException(status_code=404, detail="File not found")
    return {"content": content}


if __name__ == "__main__":
    import uvicorn  
    uvicorn.run(app, host="0.0.0.0", port=8000)
    # uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)


# cat ./data/dates.txt | while read date; do if [[ $(date -d "$date" +%A) == "Wednesday" ]]; then echo "$date"; fi done | wc -l > ./data/dates-wednesdays.txt
