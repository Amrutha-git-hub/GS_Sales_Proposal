from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
load_dotenv()
import json
from Document_Upload_Vectordb.prompts import service_extractor_template

llm = ChatGoogleGenerativeAI(model = 'gemini-1.5-flash')

from Document_Upload_Vectordb.prompts import *

from langchain_core.prompts import ChatPromptTemplate

from Document_Upload_Vectordb.doc_vectorizer import vectorize

from Document_Upload_Vectordb.doc_xtraction_utils import *

def get_services(file: str, company_name: str , client_data , seller_data):
    # Use a different variable name to avoid conflict with imported prompt
    service_extractor_prompt = ChatPromptTemplate.from_template(service_extractor_template)
    retriever = vectorize(file, company_name).as_retriever()

    # Extract the query string from input and pass to retriever
    context_chain = (
        RunnableLambda(lambda x: x["query"])  # Extract just the query string
        | retriever
        | RunnableLambda(format_docs)
    )

    rag_chain = (
        {"context": context_chain,
        "client_data": lambda x: client_data,
        "seller_data": lambda x: seller_data,}
        | service_extractor_prompt  
        | llm
        | StrOutputParser()
    )
    
    try:

        result = rag_chain.invoke({"query": "Extract key business services from this RFI."})
        print(type(json.loads(clean_to_list(result))))
        return json.loads(clean_to_list(result))
    except Exception as e:
        print(f"Error in getting services: {e}")
        return []