import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Carica variabili ambiente
load_dotenv()

app = FastAPI()

# ===== CORS CONFIGURATION =====
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*",  # Allow all origins for n8n cloud compatibility
        # Alternatively, specify n8n URL: "https://your-n8n-instance.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modello OpenAI
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.3
)

# Schema richiesta
class QueryRequest(BaseModel):
    query: str


# ===== AGENT LOGIC =====
async def run_intelligence_cycle(user_query: str) -> str:

    prompt = f"""
You are an Executive Intelligence Analyst.

Generate a professional intelligence report about:

{user_query}

Structure the report in Markdown with these sections:

## Executive Summary
## Market Overview
## Competitive Landscape
## Strategic Recommendations

Be concise and professional.
"""

    response = await llm.ainvoke(prompt)

    return response.content


# ===== API ENDPOINT =====
@app.options("/run-agent")
async def preflight_run_agent():
    """Handle CORS preflight requests"""
    return {}


@app.post("/run-agent")
async def run_agent(request: QueryRequest):
    """Main endpoint for n8n integration"""
    report = await run_intelligence_cycle(request.query)

    return {
        "report": report
    }


# ===== HEALTH CHECK =====
@app.get("/")
def root():
    return {"status": "Agent running"}