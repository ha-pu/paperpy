from modules import gpt_batch
from modules import import_pdf
from modules import remove_pattern
from modules import send_email
import shutil
import os
from dotenv import load_dotenv

load_dotenv()

input_path = 'files_new'
output_path = 'files_old'
pdf_files = [os.path.join(input_path, file) for file in os.listdir(input_path) if file.endswith('.pdf')]
pdf_files = pdf_files[:4]

texts = []
for pdf_file in pdf_files:
    if os.path.isfile(pdf_file):
        text = import_pdf.extract_text(pdf_file)
        texts.append(text)
        destination_path = os.path.join(output_path, os.path.basename(pdf_file))
        shutil.move(pdf_file, destination_path)

with open('system_prompt.txt', 'r') as f:
    system_prompt = f.read()

system_prompt = system_prompt.replace('\n', ' ')
system_prompt = system_prompt.replace('\\n', '\n')
system_prompt = system_prompt.replace('\n ', '\n')

summaries = gpt_batch.execute_batch(system_prompt, texts)
for i in range(len(summaries)):
    summaries[i] = remove_pattern.remove_pattern(summaries[i])

separator = ' <hr> '
body = separator.join(summaries)

recipient_email = os.getenv('RECEIPT_EMAIL')
subject = 'Paper Summary'

if len(body) > 0:
    send_email.send_email(recipient_email, subject, body)
