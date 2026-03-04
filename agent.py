import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from langsmith import traceable
from langchain_openai import ChatOpenAI

load_dotenv()

app = FastAPI()

# ===== MODEL =====
llm = ChatOpenAI(model="gpt-4o-mini")

# ===== REQUEST BODY =====
class QueryRequest(BaseModel):
    query: str

# ===== AGENT LOGIC =====
@traceable
def run_intelligence_cycle(user_query: str) -> str:
    prompt = f"""
    You are an Executive Intelligence Agent.

    Generate a professional intelligence report about:

    {user_query}

    Structure:
    - Executive Summary
    - Market Overview
    - Competitive Landscape
    - Strategic Recommendations
    """

    response = llm.invoke(prompt)
    return response.content

# ===== API ENDPOINT =====
@app.post("/run-agent")
async def run_agent(request: QueryRequest):
    report = run_intelligence_cycle(request.query)
    return {"report": report}