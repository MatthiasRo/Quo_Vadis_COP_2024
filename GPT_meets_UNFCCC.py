# Script: Process UNFCCC COP list of party participants to convert from unstructered TXT file into tabular format
# Author: Matthias Roesti, based on work by Pierre Chatelanaz

import os
from openai import OpenAI
import json
import pandas as pd
from tqdm import tqdm
os.environ['OPENAI_API_KEY'] = 'insert_your_openai_api_key_here_or_better_yet_store_it_safely_and_load_from_external_file'
from concurrent.futures import ProcessPoolExecutor

client_oai = OpenAI()
OpenAI.api_key = os.getenv('OPENAI_API_KEY')


# Setup - define functions
def get_flop(text: str, timeout_seconds=15) -> dict:
    # Craft a user content that instructs GPT to extract the names and further information from the raw text junks
    # and to format the output in a way that resembles HJSON for readability.
    user_content = ("I will provide you with a raw text, from which you will directly extract the following information and put it into JSON for readability with keys:"
                    "participant country: contains the country delegation of the participant (e.g. Brazil)"
                    "participant_name: contains the name of the participant"
                    "participant_prefix: contains the title of the participant (e.g. H.E., Mr., etc.)"
                    "participnat_job: contains the job description (e.g. Chief of Staff, Ambassador of Albania in France, etc.)"
                    "participant_agency_ministry: contains the Agency/ministry of the delegate (e.g. Ministry of Water Resources and Environment)"
                    "Make sure that 'participant_prefix' correctly contains the title of the person, e.g. 'Mr.,  Ms., Mrs., Dr., Prof., H.E.' etc."
                    "participant_name must not contain any title/prefix"
                    ""
                    f"{text}")
    messages = [
        {"role": "user", "content": user_content}
    ]
    
    try:
        concept_response = client_oai.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            temperature=0,  # Adjust temperature if needed for more nuanced analysis
            messages=messages,
            response_format={"type": "json_object"}, # ensures consistent response data format (JSON)
        )
        
        # This is a placeholder for response parsing logic. For now, it only extracts the result from the GPT API response
        verification_result = json.loads(concept_response.choices[0].message.content)
        
        return verification_result
    except Exception as e:
        print(f"Error in get_flop: {str(e)}")
        return {"error": "Error processing your request."}
    

def write_result(result, file_path="paris_flop_cache.jsonl"):
    with open(file_path, "a+", encoding="utf-8") as f:
        f.write(json.dumps(result) + "\n")

            
# Function to initialize an empty list to store the chunks of text, splitting wherever the text
# reads 'continued', which is on top of almost every page. The reason for this splitting
# is that GPT 3.5 doesn't do very well with longer lists/text segments (forgets many entries)
def read_and_chunk_file(filepath):
    chunks = []
    current_chunk = []

    with open(filepath, 'r') as file:
        for line in file:
            # Check if the line ends with '(continued)', strip() removes trailing newline
            if line.strip().endswith('(continued)'):
                if current_chunk:  # Add current chunk to the list if it's not empty
                    chunks.append(" ".join(current_chunk))
                current_chunk = [line]  # Start a new chunk with the current line
            else:
                current_chunk.append(line)
        # Add the last chunk if any content is left
        if current_chunk:
            chunks.append(" ".join(current_chunk))
            
    return pd.DataFrame({'text': chunks})


def split_text(text, delimiters):
    for delimiter in delimiters:
        if delimiter in text:
            # Split the text at the first occurrence of any delimiter
            parts = text.split(delimiter, 1)
            # Return two parts with the delimiter added back to the beginning of the second part
            return [parts[0], delimiter + parts[1]]
    return [text]


# loading text data
# Create a pandas DataFrame from the list of chunks
df = read_and_chunk_file('NAME_OF_FLOP_IN_TXT_FORMAT.txt')

df['length'] = df['text'].apply(len)


# Fixing entries with more than 1 page (doesn't process well on GPT 3.5), splitting into shorter segments
# Specify additional delimiters - was done manually based on the affected pages, varies by document
delimiters = ['\n Haiti \n', '\n Barbados \n', '\n Guatemala \n', '\n Jamaica \n', '\n Dominican Republic \n', '\n Croatia \n'] 

# Create an empty list to hold the new rows
new_rows = []

for _, row in df.iterrows():
    if row['length'] > 4000:
        parts = split_text(row['text'], delimiters)
        for part in parts:
            # Here, we explicitly create a new Series for each part
            new_row = pd.Series({'text': part, 'length': len(part)})
            new_rows.append(new_row)
    else:
        # If the row doesn't need to be split, we append the existing Series
        new_rows.append(row)

# Now, create a new DataFrame from the list of Series
new_df = pd.DataFrame(new_rows).reset_index(drop=True)


# Main GPT processing step
# process the data frame - this is the loop that will send junks of the txt file to the OpenAI GPT API
for i in range(0,len(new_df)):
    result = get_flop(new_df['text'][i])
    write_result(result)
    print('Done with ' + str(i))


# Post-processing: create excel sheet from JSON
data = []

# Open the .jsonl file and read line by line
with open('paris_flop_cache.jsonl', 'r') as file:
    for line in file:
        # Parse each line as JSON
        json_line = json.loads(line)
        # Extend the data list with the participants from the current line
        data.extend(json_line['participants'])

# Create a pandas DataFrame from the list of dictionaries
df = pd.DataFrame(data)


# Export the DataFrame to an Excel file
# Ensure you have 'openpyxl' installed to use the 'xlsx' writer
df.to_excel('participants.xlsx', index=False)

print("Excel file has been created successfully.")
