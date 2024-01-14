import re
import os
import csv
from tqdm import tqdm
from langchain.chat_models import ChatAnthropic
from langchain.schema import AIMessage, HumanMessage, SystemMessage
import pandas as pd

# Python code for the actual approach to request C++ translation from the ChatAnthropic API

def request_translation_to_cpp_with_api(python_code, chat_api):
    """
    Request translation of Python code to C++ using the ChatAnthropic API.
    """
    message_content = f"Translate the following Python code to C++:\n```python\n{python_code}\n```"
    messages = [SystemMessage(content=message_content)]
    
    response = chat_api(messages)
    return response.content

# Define a function to process the CSV and request translations
def process_and_save_to_csv(api_key, model_name, input_csv_path, output_csv_path):
    # Initialize the API
    anthropic_chat_api = ChatAnthropic(anthropic_api_key='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', model='claude-2')    
    # Read the input CSV
    df_input = pd.read_csv(input_csv_path)
    
    # Create a new DataFrame for storing Python code, its description, and the translated C++ code
    df_output = pd.DataFrame(columns=['python_code', 'description', 'cpp_code'])

    # Process each row in the input dataframe
    for _, row in df_input.iterrows():
        py_code = row['code']
        description = row['description']
        cpp_code = request_translation_to_cpp_with_api(py_code, anthropic_chat_api)
        
        df_output = df_output.append({
            'python_code': py_code,
            'description': description,
            'cpp_code': cpp_code
        }, ignore_index=True)

    # Save the new dataframe to the output CSV path
    df_output.to_csv(output_csv_path, index=False)
    
    print(f"Processed and saved translations to: {output_csv_path}")

def translate_python_to_cpp_and_save(api_key, model_name, input_csv_path, output_csv_path):
    # Initialize the API
    anthropic_chat_api = ChatAnthropic(anthropic_api_key=api_key, model=model_name)
    
    # Read the input CSV
    df_input = pd.read_csv(input_csv_path)
    
    # Create a dataframe for output
    df_output = pd.DataFrame(columns=["Python Code", "C++ Code", "Description"])
    
    # Translate each Python snippet and save to CSV
    for index, row in tqdm(df_input.iterrows()):
        python_code = row['code']
        description = row['description']
        
        cpp_code = request_translation_to_cpp_with_api(python_code, anthropic_chat_api)
        
        df_output = df_output.append({"Python Code": python_code, "C++ Code": cpp_code, "Description": description}, ignore_index=True)
    
    df_output.to_csv(output_csv_path, index=False)

# Call the function
translate_python_to_cpp_and_save('{anthropic_key}', 'claude', 'python_code.csv', 'cpp_translations.csv')