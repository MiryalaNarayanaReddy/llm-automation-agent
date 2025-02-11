import requests
import json


class LLMModel:
    def __init__(self, token, model):
        self.token = token
        self.model = model

    def getResponse(self,systemPrompt,userPrompt):
        url = "https://api.openai.com/v1/chat/completions"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
        }

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": systemPrompt,
                },
                {
                    "role": "user",
                    "content": userPrompt,
                },
            ],
            "temperature": 0.7,
            "max_tokens": 1000,
        }


        response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

        return response.json()
    
