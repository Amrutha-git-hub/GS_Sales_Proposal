from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from .llms import llm
from .states import State
from .utils import clean_to_list
from .prompts import *

prompt = ChatPromptTemplate.from_template(section_template)


chain = prompt | llm | StrOutputParser()




def create_sections(state:State):
    result = chain.invoke({'services':state.seller})
    p = clean_to_list(result)
    return {'sections':["Title of the sales proposal"]+p.split('\n')}
