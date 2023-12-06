import requests

API_URL = "https://api-inference.huggingface.co/models/ProsusAI/finbert"
headers = {"Authorization": "Bearer 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"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

str = input()

output = query({
	"inputs": str,
})

print(output)