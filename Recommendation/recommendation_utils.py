from langchain_core.prompts import ChatPromptTemplate
from .prompts import *
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import JsonOutputParser,StrOutputParser
from dotenv import load_dotenv
from Document_Upload_Vectordb.doc_xtraction_utils import clean_to_list
load_dotenv()
import json
from Recommendation.prompts import *

llm = ChatGoogleGenerativeAI(model = 'gemini-1.5-flash')

def clean_to_list(result:str) :
    result = result.strip()
    if result.startswith('```python'):
        result = result[len('```python'):].strip()
    elif result.startswith('```json'):
        result = result[len('```json'):].strip()
    elif result.startswith('```'):
        result = result[len('```'):].strip()
    if result.endswith('```'):
        result = result[:-3].strip()
    first_brace = result.find('{')
    if first_brace != -1:
        result = result[first_brace:]
    return result




def get_ai_client_requirements(enterprise_details,client_requirements):
    template = ChatPromptTemplate.from_template(ai_suggetion_for_additional_req_prompt)
    chain = template | llm | StrOutputParser()
    result = chain.invoke({'enterprise_details':enterprise_details,'client_requirements':client_requirements})
    return result

def get_ai_business_priorities(spoc_role="CEO"):
    template = ChatPromptTemplate.from_template(business_priotiiry_recommendation_prompt)
    chain = template | llm | JsonOutputParser()
    result = chain.invoke({'client_spoc_role':spoc_role})
    print(result)
    return result

def get_ai_proj_sepc_recommendations(prompts,client_data,seller_data):
    template = ChatPromptTemplate.from_template(prompts)
    chain = template | llm | StrOutputParser()
    result = chain.invoke({'client_data':client_data,'seller_data':seller_data})
    print(result)
    print(type(json.loads(clean_to_list(result))))
    print(json.loads(clean_to_list(result)))
    return json.loads(clean_to_list(result))


