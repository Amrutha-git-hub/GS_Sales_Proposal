from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
load_dotenv()
import json

llm = ChatGoogleGenerativeAI(model = 'gemini-1.5-flash')

from .prompts import rfi_painpoint_prompt

from langchain_core.prompts import ChatPromptTemplate

from .doc_vectorizer import vectorize

from .doc_xtraction_utils import *

def get_pain_points(file: str, company_name : str,):
    rfi_painpoint_prompt = ChatPromptTemplate.from_template(rfi_painpoint_prompt)
    retriever = vectorize(file,company_name).as_retriever()

    # Extract the query string from input and pass to retriever
    context_chain = (
        RunnableLambda(lambda x: x["query"])  # Extract just the query string
        | retriever
        | RunnableLambda(format_docs)
    )

    rag_chain = (
        {"context": context_chain}
        | rfi_painpoint_prompt
        | llm
        | StrOutputParser()
    )
    result = rag_chain.invoke({"query": "Extract key business concerns and paint points from this RFI."})
    print(type(json.loads(clean_to_list(result))))
    return json.loads(clean_to_list(result))



