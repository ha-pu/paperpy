# Project Overview

**Basic idea**: You want to get summaries of academic papers into your post box.
You put the PDF of an acdemic paper into a Dropbox folder, the script downloads
it, generates a summary, and sends it to you by email.

This repository contains a Python-based system designed to automate the process
of downloading, processing, summarizing, and emailing academic papers. The
system uses various modules to handle different tasks, including PDF text
extraction, pattern removal, and email sending. The core functionality is
controlled by a main script, `paper.py`, which integrates these modules to
achieve the desired workflow.

The workflow uses `rclone` to interact with Dropbox. This step can be
substituted by manually moving PDFs between folders.

## Folder Structure

```
working directory
├── files_new/
├── files_old/
├── logs/
├── paperpy/
└── .env
```

* **files_new**: Destination folder for PDFs downloaded from Dropbox using `rclone`.
* **files_old**: Folder where processed PDFs are moved before being uploaded back to Dropbox.
* **logs**: Contains log files (`rclone.log` and `paperpy.log`) for monitoring the script's execution.
* **paperpy**: Location of the virtual environment activated in `paperpy.sh`.

## Key Components

Scripts

* **paper.py**: Main script that coordinates the entire workflow. It extracts text from PDFs, generates summaries using GPT, removes unwanted patterns, and sends the summaries via email.
* **paperpy.sh**: Shell script to automate the execution of the main script and handle file movements using `rclone`.

Modules

* **gpt_batch.py**: Handles batch processing for generating summaries using the GPT model.
* **import_pdf.py**: Extracts text from PDF files.
* **remove_pattern.py**: Removes specific patterns from the text.
* **send_email.py**: Sends emails with the generated summaries.

Configuration Files

* **.gitignore**: Specifies files and directories to be ignored by Git.
* **requirements.txt**: Lists the Python dependencies required for the project.
* **system_prompt.txt**: Contains the prompt used by the GPT model to generate summaries.
* **README.md**: Provides an overview and instructions for the project.

## Environment Variables

The `.env` file must contain the following information:

```
OPENAI_API_KEY='XXX' # OpenAI API key
SENDER_EMAIL='XXX'   # Email from which the summary is sent
SENDER_PWD='XXX'     # Password to the e-mail account
SMTP_SERVER='XXX'    # Address of the SMTP server from which the e-mail is sent
SMTP_PORT='XXX'      # Port of the SMTP server from which the e-mail is sent
RECEIPT_EMAIL='XXX'  # Email to which the summary is sent
```

## Usage

* Setup: Ensure all dependencies are installed by running `pip install -r requirements.txt`.
* Configuration: Populate the `.env` file with the necessary environment variables.
* Execution: Run the `paperpy.sh` script to start the process. This script will:
  * Move new PDFs from Dropbox to *files_new*.
  * Activate the virtual environment.
  * Execute `paper.py` to process the PDFs and send the summaries via email.
  * Move processed PDFs to *files_old* and upload them back to Dropbox.

This setup ensures a seamless and automated workflow for handling academic
papers, from download to summary generation and email distribution.
