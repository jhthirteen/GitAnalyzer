import os
from openai import OpenAI

class GitAssistant:
    def __init__(self):
        self.client = OpenAI(api_key = os.getenv('OPEN_AI_KEY'))
        self.systemPrompt = f"""
        You are an assistant tasked with understanding a code base. You're main priorities is understanding conceptually how each file fits in with one another, what the codebase as a whole is doing and what tools / languages / frameworks are used to accomplish this, and providing summaries of each individual file that is relevant. Only stick to the infomration that is in the files. Feel free to leverage your knowledge of the languages and frameworks used, but do not extrapolate that information and make assumptions or guesses about the codebase.

        I want you to structure your output in this manner Do not explicitly write out these questions in the response, rather, use those as a guide to what content you should populate in each section. Remember, DO NOT WRITE THE QUESTIONS
        High Level Overview
        - What is the main goal of this codebase? 
        - How is it achieved? 
        - What tools, frameworks, and languages are being used? 

        Structure of the Code 
        - How is the repository structured? 
        - How does all the code fit together? 
        - How is the code deployed? How can I get this up and running by myself (NOTE: If it is not clear, do not make something up based on your knowledge)

        Individual Components
        - Give a high level overview of each file that actually contains code (please ignore configs, markdown, and other files that is not relevant to the actual code that runs) 


        You will be given the code, which contains the full file path in the GitHub repository, and then the contents of the file.   
        """

    def query(self, code):
        response = self.client.chat.completions.create(
            messages=[
                {"role" : "system", "content" : self.systemPrompt},
                {"role" : "user", "content" : code}
            ],
            model="o4-mini",
            temperature=1
        )
        content = response.choices[0].message.content
        print(content)