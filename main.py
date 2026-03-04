import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load env vars
load_dotenv()

app = FastAPI()

# CORS config to let n8n access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.3
)

class QueryRequest(BaseModel):
    query: str


@app.options("/run-agent")
async def preflight_run_agent():
    return {}


@app.post("/run-agent")
async def run_agent_endpoint(request: QueryRequest):
    # log incoming body so we can see what n8n is sending
    print("received request:", request)
    prompt = f"""
You are an Executive Intelligence Agent.

Generate a professional intelligence report about:

{request.query}

Structure:
- Executive Summary
- Market Overview
- Competitive Landscape
- Strategic Opportunities
- Risks
"""

    response = await llm.ainvoke(prompt)
    return {"report": response.content}


@app.get("/")
def root():
    return {"status": "running"}