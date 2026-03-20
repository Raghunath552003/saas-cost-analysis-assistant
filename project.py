# ================================
# Imports
# ================================
import pandas as pd
from typing import TypedDict, List, Dict
from langgraph.graph import StateGraph

# ================================
# Graph State
# ================================
class GraphState(TypedDict):
    rows: List[Dict]
    base_currency: str
    total_monthly_cost: float
    warnings: List[str]
    needs_revision: bool
    team_costs: Dict[str, float]
    tool_calls: List[Dict]


# ================================
# TOOL 1: Parse CSV
# ================================
def parse_csv_tool(csv_path):
    df = pd.read_csv(csv_path)
    return df.to_dict(orient="records")


# ================================
# TOOL 2: Normalize Billing Period
# ================================
def normalize_billing_period_tool(rows):
    for row in rows:
        bp = row["billing_period"].lower()

        if bp in ["month", "monthly"]:
            row["billing_period"] = "monthly"
        elif bp in ["year", "yearly"]:
            row["billing_period"] = "yearly"
        elif bp in ["quarter", "quarterly"]:
            row["billing_period"] = "quarterly"

    return rows


# ================================
# TOOL 3: Currency Conversion
# ================================
def convert_currency_tool(amount, from_currency, to_currency):
    rates = {
        "USD": 1,
        "INR": 0.012,
        "AED": 0.27
    }

    usd_amount = amount * rates[from_currency]
    converted = usd_amount / rates[to_currency]

    return converted


# ================================
# TOOL 4: Monthly Cost
# ================================
def compute_monthly_cost_tool(amount, billing_period):

    if billing_period == "monthly":
        return amount
    elif billing_period == "quarterly":
        return amount / 3
    elif billing_period == "yearly":
        return amount / 12
    else:
        raise ValueError("Unknown billing period")


# ================================
# AGENT 1: CSV Agent
# ================================
def csv_agent(state: GraphState):

    try:
        rows = parse_csv_tool("data/subscriptions.csv")

        # log tool call
        state["tool_calls"].append({
            "tool_name": "parse_csv_tool",
            "agent_name": "csv_agent",
            "purpose": "Read CSV file"
        })
        rows = normalize_billing_period_tool(rows)

         # log tool call
        state["tool_calls"].append({
            "tool_name": "normalize_billing_period_tool",
            "agent_name": "csv_agent",
            "purpose": "Normalize billing periods"
        })

        state["rows"] = rows

    except Exception as e:
        state["warnings"].append(str(e))
        state["needs_revision"] = True

    return state


# ================================
# AGENT 2: Cost Analysis
# ================================
def cost_analysis_agent(state: GraphState):

    rows = state["rows"]
    base_currency = state["base_currency"]

    total_monthly_cost = 0
    team_costs = {}
    updated_rows = []

    for row in rows:
        try:
            # currency conversion
            converted_price = convert_currency_tool(
                row["price"],
                row["currency"],
                base_currency
            )
            state["tool_calls"].append({
                "tool_name": "compute_monthly_cost_tool",
                "agent_name": "cost_agent",
                "purpose": f"{row['name']} - convert {row['billing_period']} to monthly"
            })
            # monthly cost
            monthly_cost = compute_monthly_cost_tool(
                converted_price,
                row["billing_period"]
            )
            state["tool_calls"].append({
                "tool_name": "compute_monthly_cost_tool",
                "agent_name": "cost_agent",
                "purpose": f"{row['name']} - convert {row['billing_period']} to monthly"
            })

            monthly_cost = round(monthly_cost, 2)

            row["monthly_cost"] = monthly_cost
            total_monthly_cost += monthly_cost

            
            # team breakdown
            team = row.get("team", "Unknown")

            if team not in team_costs:
                team_costs[team] = 0

            team_costs[team] = round(team_costs[team] + monthly_cost, 2)

            updated_rows.append(row)

        except Exception as e:
            state["warnings"].append(str(e))

    state["rows"] = updated_rows
    state["total_monthly_cost"] = round(total_monthly_cost, 2)
    state["team_costs"] = team_costs

    return state


# ================================
# AGENT 3: Safety Agent
# ================================
def safety_agent(state: GraphState):

    rows = state["rows"]
    total = state["total_monthly_cost"]

    calculated_total = sum([row["monthly_cost"] for row in rows])

    # check mismatch
    if abs(calculated_total - total) > 0.01:
        state["warnings"].append("Mismatch in total cost")
        state["needs_revision"] = True

    # negative check
    for row in rows:
        if row["monthly_cost"] < 0:
            state["warnings"].append("Negative cost detected")
            state["needs_revision"] = True

        if row["monthly_cost"] is None:
            state["warnings"].append("Missing cost value")
            state["needs_revision"] = True

    return state


# ================================
# BUILD GRAPH
# ================================
builder = StateGraph(GraphState)

builder.add_node("csv_agent", csv_agent)
builder.add_node("cost_agent", cost_analysis_agent)
builder.add_node("safety_agent", safety_agent)

builder.set_entry_point("csv_agent")

builder.add_edge("csv_agent", "cost_agent")
builder.add_edge("cost_agent", "safety_agent")

builder.set_finish_point("safety_agent")

graph = builder.compile()