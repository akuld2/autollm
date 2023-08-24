import re
import os
import csv
from tqdm import tqdm
from langchain.chat_models import ChatAnthropic
from langchain.schema import AIMessage, HumanMessage, SystemMessage

def parse_snippet(message):
    def extract_code_and_description(message):
        pattern = r'```python\n(.*?)\n```\n\n(.*?)$'
        match = re.search(pattern, message, re.DOTALL)
        
        if match:
            code = match.group(1).strip()
            description = match.group(2).strip()
            return code, description
        else:
            return None, None

    code, description = extract_code_and_description(message)
    if (code is not None) and (description is not None):
        with open('python_code.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow([code, description])

anthropic_chat = ChatAnthropic(anthropic_api_key='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', model='claude-2')

with open('python_code.csv', 'a') as f:
    if os.stat('python_code.csv').st_size == 0:
        writer = csv.writer(f)
        writer.writerow(['code', 'description'])

def generate_one_snippet():
    messages = [
        SystemMessage(content="Generate a medium-length, correct, and unique Python code snippet. The code snippet should be well-formatted and easy to understand. It should also demonstrate good coding practices. The topic of the code snippet should be chosen at random from a diverse range of subjects. Do not generate code using the \"import random\" library. The code snippet should be different from any previously generated snippets. Do not use any external libraries in your code snippet apart from python builtins. Do not print anything before printing your code. After printing the code, provide a brief explanation on what the code does."),
    ]
    response = anthropic_chat(messages)
    return response.content

def generate_unique_snippets(n):
    for _ in tqdm(range(n), desc="Generating code"):
        while True:
            snippet = generate_one_snippet()
            parse_snippet(snippet)
            break

generate_unique_snippets(10000)