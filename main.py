from fastapi import FastAPI
from pydantic import BaseModel
from agent import run_agent

app = FastAPI()


class QueryRequest(BaseModel):
    query: str


@app.post("/run-agent")
def execute_agent(request: QueryRequest):
    report = run_agent(request.query)
    return {"report": report}