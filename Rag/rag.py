from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
load_dotenv()
import json

llm = ChatGoogleGenerativeAI(model = 'gemini-1.5-flash')



template  = """
You are a highly capable business analyst AI with deep expertise in sales, technology, and market research. Your task is to analyze an RFI (Request for Information) document from a client who is seeking digital or technology solutions.

From this document, extract and synthesize **three key insights or business pain points** that the client organization is implicitly or explicitly concerned about. Each pain point should be labeled under a relevant category, followed by a brief, insightful summary.

Your output should strictly follow this format:

Here is the context of the salse proposal : {context}

return {{
    "Category1": "Insightful and concise pain point summary for this category.",
    "Category2": "Another brief insight under a different relevant category.",
    "Category3": "A third meaningful insight under its appropriate category.",
}}

Only output this JSON-style dictionary — no explanations or additional text. Ensure the insights are useful to a product strategist or sales proposal team.
"""
rfi_painpoint_prompt = ChatPromptTemplate.from_template(template)

from langchain_core.prompts import ChatPromptTemplate

from .utils import vectorize

def format_docs(docs):
    return '\n\n'.join(doc.page_content for doc in docs)

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
    return result


def get_pain_points(file: str,company_name : str):
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

