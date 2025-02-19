import requests
import json
import numpy as np

class LLMModel:
    def __init__(self, model, token, tools):
        self.base_url = "https://aiproxy.sanand.workers.dev/"
        self.model = model
        self.token = token
        self.tools = tools
        self.systemPrompt =  ""

    def parseTask(self, prompt):
        url = f"{self.base_url}/openai/v1/chat/completions"

        headers={"Authorization": f"Bearer {self.token}"}

        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": self.systemPrompt},
                {"role": "user", "content": prompt}],
            "functions": self.tools,
            "function_call": "auto"  # Let the model decide when to call a function
        }

        response = requests.post(url=url, headers=headers, json=payload,verify=False)

        return response.json()

    def getResponse(self, system_prompt, user_prompt, base64_image=None):
        url = f"{self.base_url}/openai/v1/chat/completions"

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
    

    def get_similarity_matrix(self, docs):
        URL = f"{self.base_url}/openai/v1/embeddings"
        
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "text-embedding-3-small",
            "input": docs,
        }
        
        response = requests.post(URL, headers=headers, json=data)
        _embeddings = response.json()
        embeddings = np.array([d["embedding"] for d in _embeddings["data"]])
        similarity_matrix = embeddings @ embeddings.T
        np.fill_diagonal(similarity_matrix, -np.inf)
        return similarity_matrix
    
    def getMostSimilarDocs(self, docs, n=3):
        similarity_matrix = self.get_similarity_matrix(docs)
        pairs = []
        
        for i in range(len(docs)):
            for j in range(i + 1, len(docs)):
                pairs.append((similarity_matrix[i][j], docs[i], docs[j]))
        
        pairs.sort(reverse=True, key=lambda x: x[0])
        top_pairs = pairs[:n]
        top_sentences = [pair[1] for pair in top_pairs]
        
        return top_sentences
    
    def fix_request(self, prompt, error_message, failed_command):
        url = f"{self.base_url}/openai/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        
        # Construct message list
        messages = [
            {"role": "system", "content": self.systemPrompt},
            {"role": "user", "content": prompt}
        ]
      
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": self.systemPrompt},
                {"role": "user", "content": prompt}],
            "functions": self.tools,
            "function_call": "auto"  # Let the model decide when to call a function
        }

        # Make request
        response = requests.post(url=url, headers=headers, json=payload, verify=False)

        return response.json()  
    
    def transcribeAudio(self, file_path):
        url = f"{self.base_url}/openai/v1/audio/transcriptions"
        headers = {"Authorization": f"Bearer {self.token}"}
        files = {"file": open(file_path, "rb")}
        data = {"model": "whisper-1"}
        response = requests.post(url, headers=headers, files=files, data=data)
        return response.json()
    
    def parseTranscription(self, transcription_response):
        parsed_data = {
            "task": transcription_response.get("task", ""),
            "language": transcription_response.get("language", ""),
            "duration": transcription_response.get("duration", 0),
            "text": transcription_response.get("text", ""),
            "segments": [
                {
                    "start": segment.get("start", 0),
                    "end": segment.get("end", 0),
                    "text": segment.get("text", "")
                } for segment in transcription_response.get("segments", [])
            ],
            "request_id": transcription_response.get("x_groq", {}).get("id", "")
        }
        
        # get transcription text
        transcription_text = parsed_data["text"]

        return transcription_text
    
    def scrapeWebsite(self, website_code,system_prompt):
        url = f"{self.base_url}/openai/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        
        # Construct message list
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": website_code}
        ]
      
        payload = {
            "model": "gpt-4o-mini",
            "messages": messages
        }

        # Make request
        response = requests.post(url=url, headers=headers, json=payload, verify=False)

        res = response.json()

        response_data = res.get("choices")[0].get("message").get("content").strip()

        return response_data