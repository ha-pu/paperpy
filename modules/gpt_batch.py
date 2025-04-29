import json
import openai
import os
import time
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
client = openai.OpenAI()

def execute_batch(system, lst_user):
    """
    Executes a batch process for generating chat completions using the GPT model.
    Args:
        system (str): The system message to be included in the chat completion.
        lst_user (list): A list of user messages to be included in the chat completion.
    Returns:
        list: A list of summaries generated from the chat completions.
    Raises:
        Exception: If the batch process fails.
    The function performs the following steps:
        1. Prepares a JSONL file with the input data.
        2. Uploads the JSONL file to the server.
        3. Removes the local JSONL file.
        4. Starts the batch process.
        5. Polls the server for the batch status until it is completed.
        6. Retrieves the batch results.
        7. Writes the results to a local JSONL file.
        8. Reads the results from the local JSONL file.
        9. Removes the local JSONL file.
        10. Extracts and returns the summaries from the results.
    """
    file_name = 'paperpy.jsonl'

    # prepare jsonl file
    idx = 1
    for i in lst_user:
        json_content = {
            'custom_id': 'paperpy' + str(idx),
            'method': 'POST',
            'url': '/v1/chat/completions',
            'body': {
                'model': 'gpt-4.1-nano',
                'messages': [
                    {'role': 'system', 'content': system},
                    {'role': 'user', 'content': i},
                ]
            }
        }
        with open(file_name, 'a') as f:
            f.write(json.dumps(json_content) + '\n')
        idx = idx + 1
    
    print('JSONL file prepared.')
    
    # upload jsonl file
    input_file = client.files.create(
        file=open(file_name, 'rb'),
        purpose='batch'
    )
    print('JSONL file uploaded.')

    # remove jsonl file
    os.remove(file_name)

    # start batch
    batch = client.batches.create(
        input_file_id=input_file.id,
        endpoint='/v1/chat/completions',
        completion_window='24h',
        metadata={'description': 'nightly eval job'}
    )
    print('Batch submitted.')

    # get batch results
    status_flag = 'processing'
    while status_flag != 'completed':
        time.sleep(5)
        results = client.batches.retrieve(batch.id)
        status_flag = results.status
        if status_flag == 'failed':
            raise Exception('Batch error!')
    
    results = client.files.content(results.output_file_id)

    with open(file_name, 'w') as f:
        f.write(results.text)

    with open(file_name, 'r') as f:
        results = f.readlines()
    
    # remove jsonl file
    os.remove(file_name)

    summaries = []
    for i in results:
        result = json.loads(i)
        result = result['response']['body']['choices'][0]['message']['content']
        summaries.append(result)
    
    return summaries
