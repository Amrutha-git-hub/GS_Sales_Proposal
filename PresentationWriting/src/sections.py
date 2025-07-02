from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from .llms import llm
from .states import State
from .utils import clean_to_list

template = '''You are a business consultant specialized in drafting professional sales proposals.

Based on the following services offered by the client, generate a list of high-level sections that should be included in a compelling business proposal. These sections should be relevant to the domain and type of services offered.

### Services:
{services}

Return only a clean list of section titles, no explanations or numbering.

IMPORTANT :
Dont put too much sections just include the important ones like the most necessary and not to forget Scope of work / Project breakdown 

'''
prompt = ChatPromptTemplate.from_template(template)


chain = prompt | llm | StrOutputParser()




def create_sections(state:State):
    result = chain.invoke({'services':state.seller})
    p = clean_to_list(result)
    return {'sections':["Title of the sales proposal"]+p.split('\n')}
