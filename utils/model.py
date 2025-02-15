import requests
import json


class LLMModel:
    def __init__(self, model, token, tools):
        self.model = model
        self.token = token
        self.tools = tools

    def parseTask(self, prompt):
        url = "https://llmfoundry.straive.com/openai/v1/chat/completions"

        headers={"Authorization": f"Bearer {self.token}"}

        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": '''You are an automation agent.You have to understand the given task and if it is in the list of function tools then return the correct arguments and function names. If there are any paths then make sure to return the same without changing or adding anything.'''},
                {"role": "user", "content": prompt}],
            "functions": self.tools,
            "function_call": "auto"  # Let the model decide when to call a function
        }

        response = requests.post(url=url, headers=headers, json=payload,verify=False)

        return response.json()

    def getResponse(self, system_prompt, user_prompt, base64_image=None):
        url = "https://llmfoundry.straive.com/openai/v1/chat/completions"

        headers={"Authorization": f"Bearer {self.token}"}
        
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}],
        }

        #  if base64_image:
        # messages.append({"role": "user", "content": "Here is the image:", "images": [base64_image]})

        if base64_image:
            payload["messages"]["images"] = [base64_image]

        response = requests.post(url=url, headers=headers, json=payload,verify=False)

        return response.json()
        
    
