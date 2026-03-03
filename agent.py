import os
from typing import TypedDict
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langsmith import traceable

load_dotenv()


# -------------------------
# STATE
# -------------------------

class AgentState(TypedDict):
    query: str
    report: str


# -------------------------
# MODEL
# -------------------------

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.3
)


# -------------------------
# PROMPT
# -------------------------

ANALYST_SYSTEM_PROMPT = """
You are a senior AI industry analyst writing for C-suite executives.
Your job is to transform research into a structured executive intelligence briefing.

Output must be professional Markdown.
Include:
- Executive Summary
- Key Developments
- Strategic Implications
- Risks
- Recommended Actions
"""


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", ANALYST_SYSTEM_PROMPT),
        ("human", "{query}")
    ]
)


# -------------------------
# AGENT FUNCTION (TRACED)
# -------------------------

@traceable(name="ai_market_agent_run")
def run_agent(query: str) -> str:
    chain = prompt | llm
    response = chain.invoke({"query": query})
    return response.content