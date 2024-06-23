import requests
import json
import os
from dotenv import load_dotenv
from tkinter import filedialog

load_dotenv()

url = os.getenv('url')
auth_key = os.getenv("auth_key")

class ResumeLatexGenerator:
    def __init__(self):
        pass

    def get_latex(self, data: str, template: str, prompt=None) -> str:
        """Generates a LaTeX template for the user's resume.

        Args:
            data (str): The user's information.
            template (str): The LaTeX example file.
            prompt (str, optional): The prompt for the model. Defaults to None.

        Returns:
            str: The generated LaTeX file for the user's resume.
        """
        if prompt is None:
            prompt = r"You are a resume writing tutor. Your job is to generate a LaTeX template for the user's resume. You will be given some information about the user and a LaTeX example file, and you should apply the user's information to replace the information in the example file. If the needed information is missing, you can remove that part. The response should be in .tex format. Always make sure that the returned LaTeX file is VALID. Always follow the original template format. DO NOT forget the \begin{document}"
        if url is None or auth_key is None:
            return Exception("Please set the url and auth_key in the .env file")
        
        try:
            payload = json.dumps({
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "system",
                    "content": prompt
                },
                {
                    "role": "user",
                    "content": "User information: " + data + "\n\nLaTeX example file: " + template
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
        
        except Exception as e:
            return e
    

if __name__ == '__main__':
    resume_latex_generator = ResumeLatexGenerator()

    data = "" # please provide the user's information
    template = "" # please provide the LaTeX example file
    filename = "output/resume.tex"

    if len(data) == 0:
        with open(filedialog.askopenfilename(title="Select the user's information file", filetypes=[("CSV files", "*.csv")]), 'r', encoding="utf-8") as file:
            data = file.read()

    if len(template) == 0:
        with open(filedialog.askopenfilename(title="Select the LaTeX example file", filetypes=[("LaTeX files", "*.tex")]), 'r', encoding="utf-8") as file:
            template = file.read()

    reply_text = resume_latex_generator.get_latex(data, template) 
    #print(reply_text)
    with open(filename, 'w', encoding="utf-8") as file:
        file.write(reply_text)
