from pydantic import BaseModel,Field
from typing import *
import operator


class State(BaseModel):
    client : Any
    seller :Any
    project_specs : Any
    sections : List[str] 
    final_result : str 
    output_file_path: str = ""

