"""
Note: this rater utlizes gpt-3.5, so it cannot take files as input. Therefore, only the text but not the format is considered.
"""


import requests
import json
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv('url')
auth_key = os.getenv("auth_key")

class ResumeRater:
	def __init__(self):
		pass

	def get_advice(self, theme: str, content: str) -> str:
		payload = json.dumps({
		"model": "gpt-3.5-turbo",
		"messages": [
			{
				"role": "system",
				"content": "You are a resume writing tutor. Your job is to pretend that you are a professional human resource manager who hires new employees. You need to read the resume and then provide a rating (at the scale of 0-100) and some feedback on how to improve the resume. You can also provide feedback on having the user remove unrelated experience and/or includes most recent activities. The user is writing a resume for " + str(theme) + "Current date: " + str(datetime.date.today())
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
		
		try:
			response = json.loads(requests.request("POST", url, headers=headers, data=payload).text)
			
			#print(response)
			reply_text = response["choices"][0]["message"]["content"]
			
			return reply_text
		
		except Exception as e:
			return e
	

if __name__ == '__main__':
	resume_rater = ResumeRater()

	theme = "" # please briefly describe what the resume is for. E.g., a research assistant position in Computer Science, a part-time in restaurant
	content = "" # please paste the content of the resume

	if len(theme) == 0:
		theme = input("Please briefly describe what the resume is for. E.g., a research assistant position in Computer Science, a part-time in restaurant:")

	if len(content) == 0:
		content = input("Please paste the content of the resume:")

	reply_text = resume_rater.get_advice(theme, content)
	print(reply_text)
