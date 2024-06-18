import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv('url')
auth_key = os.getenv("auth_key")

def get_advice(content: str) -> str:
	payload = json.dumps({
	   "model": "gpt-3.5-turbo",
	   "messages": [
	      {
	        "role": "system",
	        "content": "You are a resume writing tutor. Your job is to improve the quality of the user's resume and make the expression as professional and human-like as possible, while not distorting the truth."
	      },
	      {
	        "role": "user",
	        "content": content
	      }
	   ]
	})
	headers = {
	   'Authorization': 'Bearer ' + auth_key,
	   'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
	   'Content-Type': 'application/json'
	}
	
	response = json.loads(requests.request("POST", url, headers=headers, data=payload).text)
	
	#print(response)
	reply_text = response["choices"][0]["message"]["content"]
	
	return reply_text
	

if __name__ == '__main__':

	content = "" # please paste the content of the resume

	if len(content) == 0:
		content = input("Please paste the content of the resume:")

	reply_text = get_advice(content)
	print(reply_text)
