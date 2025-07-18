from google.adk.agents import Agent
from google.adk.tools import google_search
from pydantic import BaseModel,Field
from dotenv import load_dotenv
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
import ast 
import re
from Search.WebsiteUrl_Agent.agent_prompts import *



load_dotenv()

import os 
os.environ["GOOGLE_API_KEY"] ="AIzaSyDTYADVQVxJ5-UKQYZ8-tNFDlo-SKhwzEU"

class WebSite(BaseModel):
    website_name : str = Field(description="Website name")
    website_url : str = Field(description="Website url")


search_agent = Agent(
    model='gemini-2.0-flash-001',
    name='url_agent',
    description=description,
   instruction = instruction,
    tools = [google_search],
)

