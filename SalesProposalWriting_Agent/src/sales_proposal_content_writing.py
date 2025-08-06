from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from .llms import llm
from .states import State
from .prompts import *




# Set up LangChain prompt + parser
p_prompt = ChatPromptTemplate.from_template(proposal_template)
p_chain = p_prompt | llm | StrOutputParser()

# Function to generate the full proposal
def write_sales_proposal(state:State):
    section_string = "\n".join([f"- {s}" for s in state.sections])

    result = p_chain.invoke({
        'client_details':state.client,
        'seller_details':state.seller,
        'project_specs':state.project_specs,
        'section_list':section_string

    })

    return {'final_result': result}
