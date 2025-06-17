from google.adk.agents import Agent
from google.adk.tools import google_search
from pydantic import BaseModel,Field
from dotenv import load_dotenv
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
import ast 
import re


load_dotenv()
class WebSite(BaseModel):
    website_name : str = Field(description="Website name")
    website_url : str = Field(description="Website url")


search_agent = Agent(
    model='gemini-2.0-flash-001',
    name='url_agent',
    description = (
    "You are an intelligent assistant specialized in finding official and relevant websites "
    "associated with a given organization or company name. Your goal is to retrieve high-quality, "
    "credible links that accurately represent the digital presence of the organization."
),
   instruction = '''
    Given the name of a company or organization, your task is to search and return the top 7 most relevant and credible website URLs associated with it.

    These can include:
    - The official company website try fetching this and if there are multiple then show all 7


    Your response must be a clean Python-style list of strings, where each string is a valid URL.

    Format your response exactly like this:

    [
    "https://google.com/",
    "https://cloud.google.com",
    "https://accounts.google.com"
    ]

    Like this any 10 urls that are related to the given organization name

    Do not include explanations, only return the list of URLs.

    IMPORTANT : Just return me list of urls no additional text

    return like 
   
    
    ----
        [
    "https://google.com/",
    "https://cloud.google.com",
    "https://accounts.google.com"
    ]

    ----

    VERY IMPORTANT : TEMPERATURE OF THE MODEL BE ZEROOOO AND remember dont give me like the links of youtube or linkedin or any other platforms
    THE LINK SHOULD BE OFFICIAL LINK OF THE ORGANIZATION
    ''',

    tools = [google_search],
)



# Setup session and runner
session_service = InMemorySessionService()
SESSION_ID = 'sess'
USER_ID = 'user'

session = session_service.create_session(
    app_name="APP",
    user_id=USER_ID,
    session_id=SESSION_ID
)

runner = Runner(
    app_name="APP",
    session_service=session_service,
    agent=search_agent
)
def extract_list_from_string(s):
    # Remove any prefix like 'json' and extract the JSON array part
    match = re.search(r"\[.*\]", s, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            print("Failed to parse list.")
    else:
        print("No list found.")
    return None


import json
async def get_urls(company_name: str, runner=runner, user_id=USER_ID, session_id=SESSION_ID):
    content = types.Content(role='user', parts=[types.Part(text=company_name)])
    final_msg = ""
    
    async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):
        if event.is_final_response():
            if event.content and event.content.parts:
                final_msg = event.content.parts[0].text
            elif event.actions and event.actions.escalate:
                final_msg = event.error_message
    result = final_msg
    result = result.strip()
    if result.startswith('```python'):
        result = result[len('```python'):].strip()
    elif result.startswith('```json'):
        result = result[len('```json'):].strip()
    elif result.startswith('```'):
        result = result[len('```'):].strip()
    if result.endswith('```'):
        result = result[:-3].strip()
    final_msg = result
    print(final_msg)
    return json.loads(final_msg)

import asyncio
asyncio.run(get_urls("growth sutra"))