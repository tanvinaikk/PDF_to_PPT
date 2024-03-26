from openai import OpenAI

client = OpenAI(api_key="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")
import os
import typing

# Set OpenAI API key
# openai.api_key = os.getenv("OPENAI_KEY")

def gpt_divide(text):
    completion = client.chat.completions.create(model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content" : "I am giving you a paragraph. return a it in 6 topics of parts - introduction, Literature Review, Methodology, Results, Discussion, Conclusion where every topic must have 4 points. strictly follow the syntax 'Topic: topic goes here, Points: all the points'. make the points ppt-friendly and concise."},
        {"role": "user", "content" : text}
    ])
    return completion.choices[0].message.content
