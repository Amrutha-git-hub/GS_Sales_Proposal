from langchain_core.prompts import ChatPromptTemplate
from .prompts import *
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
load_dotenv()

llm = ChatGoogleGenerativeAI(model = 'gemini-1.5-flash')




def get_ai_client_requirements(enterprise_details,client_requirements):
    template = ChatPromptTemplate.from_template(ai_suggetion_for_additional_req_prompt)
    chain = template | llm | StrOutputParser()
    result = chain.invoke({'enterprise_details':enterprise_details,'client_requirements':client_requirements})
    return result

def get_ai_business_priorities(spoc_role):
    template = ChatPromptTemplate.from_template(business_priotiiry_recommendation_prompt)
    chain = template | llm | StrOutputParser()
    result = chain.invoke({'client_spoc_role':spoc_role})
    return result
