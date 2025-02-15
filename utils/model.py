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
                {"role": "system", "content": '''You are an automation agent. If there are any paths then make sure to return the same without changing or adding anything.'''},
                {"role": "user", "content": prompt}],
            "functions": self.tools,
            "function_call": "auto"  # Let the model decide when to call a function
        }

        response = requests.post(url=url, headers=headers, json=payload,verify=False)

        return response.json()

    def getResponse(self, system_prompt, user_prompt, base64_image=None):
        url = "https://llmfoundry.straive.com/openai/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        
        # Construct message list
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": [{"type": "text", "text": user_prompt}]}
        ]

        # Append image content if provided
        if base64_image:
            messages[1]["content"].append(
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
            )

        # Payload with corrected structure
        payload = {
            "model": "gpt-4o-mini",
            "messages": messages
        }

        # Make request
        response = requests.post(url=url, headers=headers, json=payload, verify=False)

        return response.json()
    
