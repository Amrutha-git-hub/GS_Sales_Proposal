
from .utils import clean_to_list
from .states import State 
import ast 



def clean_data(state:State):
    result = clean_to_list(state.final_result)
    result = ast.literal_eval(result)
    
    with open('output.txt', 'w', encoding='utf-8') as f:
        for entry in result:
            f.write(f"Title: {entry['title']}\n")
            f.write(f"Text: {entry['text']}\n\n")
        
