from project import graph

initial_state = {
    "rows": [],
    "base_currency": "USD",
    "total_monthly_cost": 0,
    "warnings": [],
    "needs_revision": False,
    "team_costs": {},
    "tool_calls": []
}

result = graph.invoke(initial_state)


from pydantic import BaseModel
from typing import List, Dict

class FinalCostReport(BaseModel):
    base_currency: str
    total_monthly_cost: float
    warnings: List[str]
    needs_revision: bool
    rows: List[Dict]
    team_costs: Dict[str, float]
    tool_calls: List[Dict]

report = FinalCostReport(**result)

print(report.model_dump_json(indent=2))