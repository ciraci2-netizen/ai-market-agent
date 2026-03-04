import os
import time
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from tavily import TavilyClient
from pinecone import Pinecone
from openai import OpenAI

load_dotenv()

# ------------------------------------------------
# INITIALIZE SERVICES
# ------------------------------------------------

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.3
)

tavily = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)

pinecone_client = Pinecone(
    api_key=os.getenv("PINECONE_API_KEY")
)

pinecone_index = pinecone_client.Index("ai-agent-reports")

openai_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# ------------------------------------------------
# RETRY HELPER
# ------------------------------------------------

async def retry_llm_call(prompt, retries=3):

    for attempt in range(retries):

        try:

            response = await llm.ainvoke(prompt)
            return response.content

        except Exception as e:

            if attempt < retries - 1:

                print(f"Retry {attempt+1}/{retries}")
                time.sleep(3)

            else:

                raise e


# ------------------------------------------------
# WEB SEARCH
# ------------------------------------------------

def search_web(topic):

    try:

        results = tavily.search(
            query=topic,
            search_depth="advanced",
            max_results=3
        )

        context = "\n".join([
            f"- {r['title']}: {r['content']}"
            for r in results["results"]
        ])

        return context

    except Exception as e:

        print("Search error:", e)
        return "No live search results."


# ------------------------------------------------
# SAVE MEMORY (PINECONE)
# ------------------------------------------------

def save_report_to_memory(query, report):

    try:

        embedding = openai_client.embeddings.create(
            input=report,
            model="text-embedding-3-large"
        )

        pinecone_index.upsert([
            {
                "id": str(time.time()),
                "values": embedding.data[0].embedding,
                "metadata": {
                    "query": query,
                    "summary": report[:500]
                }
            }
        ])

    except Exception as e:

        print("Memory save failed:", e)


# ------------------------------------------------
# MAIN AGENT FUNCTION
# ------------------------------------------------

async def run_intelligence_cycle(user_query: str) -> str:

    print("Starting intelligence cycle")

    # 1️⃣ Web Research
    research_data = search_web(user_query)

    prompt = f"""
You are an Executive Intelligence Agent.

Generate a professional strategic intelligence report.

TOPIC:
{user_query}

LIVE MARKET SIGNALS:
{research_data}

STRUCTURE:

# Executive Summary
Explain the most important development.

# Market Overview
Explain current industry situation.

# Competitive Landscape
Major companies and positioning.

# Strategic Opportunities
Business opportunities emerging.

# Risks
Strategic risks companies must watch.

# Impact Score (1-10)

Write like a consulting firm (McKinsey style).
"""

    # 2️⃣ LLM Analysis
    report = await retry_llm_call(prompt)

    # 3️⃣ Save to Pinecone
    save_report_to_memory(user_query, report)

    return report