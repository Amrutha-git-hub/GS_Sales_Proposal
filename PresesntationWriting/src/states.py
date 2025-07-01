from pydantic import BaseModel,Field
from typing import *
import operator


class State(BaseModel):
    client : Any
    seller :Any
    project_specs : List[str]
    sections : List[str] 
    final_result : str 
    