
from .utils import clean_to_list
from .states import State 
import ast 
from dotenv import load_dotenv
import os 
load_dotenv()


output_path = os.getenv("OUTPUT_FILE_PATH")


def clean_data(state:State):
    result = clean_to_list(state.final_result)
    result = ast.literal_eval(result)
    # for the output file use client_seller_datetime.txt
    
    with open(state.output_file_path, 'w', encoding='utf-8') as f:
        for entry in result:
            f.write(f"Title: {entry['title']}\n")
            f.write(f"Text: {entry['text']}\n\n")
      