import openai
import os
import typing

# Set OpenAI API key
# openai.api_key = os.getenv("OPENAI_KEY")
openai.api_key = "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"

def gpt_summarise(text):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content" : "I am giving you a paragraph. return a it in 6 topics of parts - introduction, Literature Review, Methodology, Results, Discussion, Conclusion where every topic must have 4 points. strictly follow the syntax 'Topic: topic goes here, Points: all the points'. make the points ppt-friendly and concise."},
            {"role": "user", "content" : text}
        ]
    )
    return completion['choices'][0]['message']['content']
