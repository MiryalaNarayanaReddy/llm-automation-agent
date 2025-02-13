import requests
import json


class LLMModel:
    def __init__(self, model, token, tools):
        self.model = model
        self.token = token
        self.tools = tools

    def getResponse(self, prompt):
        url = "https://llmfoundry.straive.com/openai/v1/chat/completions"

        headers={"Authorization": f"Bearer {self.token}:tds-course"}

        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "You are an automation agent. You have to write executable bash commands, python code snippets and python scripts. Make sure sure that the read/write paths are inside the ./data directory. if user says /data then use the ./data directory. Python code can have multiple lines. Make sure to use the correct indentation. Bash commands should be common and should not have new commands which can't be found or installed. if there is a chance it's not avaiable then have it installed first. Make sure to return in the format in function calls do no return text or content"},
                {"role": "user", "content": prompt}],
            "functions": self.tools,
            "function_call": "auto"  # Let the model decide when to call a function
        }

        response = requests.post(url=url, headers=headers, json=payload,verify=False)

        return response.json()
    
