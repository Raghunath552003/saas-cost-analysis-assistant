# SaaS Cost Analysis Assistant

## Overview
This project implements a multi-agent AI workflow using LangGraph to analyze SaaS subscription costs.

## Features
- CSV ingestion and normalization
- Currency conversion
- Monthly cost calculation
- Team-wise cost breakdown
- Safety validation
- Structured JSON output using Pydantic

## Architecture
- CSV Agent
- Cost Analysis Agent
- Safety Agent

## Design Decisions
- Used LangGraph to structure multi-agent workflow
- Used simple Python functions as tools for clarity
- Chose fixed exchange rates for simplicity

## Trade-offs
- Exchange rates are static (not real-time)
- Limited error handling for edge cases
- No database integration

## Limitations
- Does not handle large-scale datasets
- No UI or API interface
- Currency conversion is approximate

## How to Run
```bash
python main.py

## Example  JSON Output
{
  "base_currency": "USD",
  "total_monthly_cost": 294.95,
  "warnings": [],
  "needs_revision": false,
  "rows": [
    {
      "name": "Vercel Pro",
      "description": "Hosting platform",
      "team": "Engineering",
      "billing_period": "monthly",
      "price": 20,
      "currency": "USD",
      "monthly_cost": 20.0
    },
    {
      "name": "Notion",
      "description": "Workspace tool",
      "team": "Marketing",
      "billing_period": "yearly",
      "price": 120,
      "currency": "INR",
      "monthly_cost": 0.12
    },
    {
      "name": "Figma",
      "description": "Design tool",
      "team": "Design",
      "billing_period": "quarterly",
      "price": 15,
      "currency": "AED",
      "monthly_cost": 1.35
    },
    {
      "name": "AWS",
      "description": "Cloud infrastructure",
      "team": "Engineering",
      "billing_period": "monthly",
      "price": 200,
      "currency": "USD",
      "monthly_cost": 200.0
    },
    {
      "name": "Slack",
      "description": "Team communication",
      "team": "HR",
      "billing_period": "yearly",
      "price": 240,
      "currency": "INR",
      "monthly_cost": 0.24
    },
    {
      "name": "Zoom",
      "description": "Video meetings",
      "team": "HR",
      "billing_period": "monthly",
      "price": 15,
      "currency": "USD",
      "monthly_cost": 15.0
    },
    {
      "name": "GitHub",
      "description": "Code hosting",
      "team": "Engineering",
      "billing_period": "monthly",
      "price": 25,
      "currency": "USD",
      "monthly_cost": 25.0
    },
    {
      "name": "Jira",
      "description": "Project management",
      "team": "Engineering",
      "billing_period": "quarterly",
      "price": 90,
      "currency": "AED",
      "monthly_cost": 8.1
    },
    {
      "name": "HubSpot",
      "description": "Marketing automation",
      "team": "Marketing",
      "billing_period": "yearly",
      "price": 300,
      "currency": "USD",
      "monthly_cost": 25.0
    },
    {
      "name": "Google Workspace",
      "description": "Email and collaboration",
      "team": "Operations",
      "billing_period": "monthly",
      "price": 12,
      "currency": "INR",
      "monthly_cost": 0.14
    }
  ],
  "team_costs": {
    "Engineering": 253.1,
    "Marketing": 25.12,
    "Design": 1.35,
    "HR": 15.24,
    "Operations": 0.14
  },
  "tool_calls": [
    {
      "tool_name": "parse_csv_tool",
      "agent_name": "csv_agent",
      "purpose": "Read CSV file"
    },
    {
      "tool_name": "normalize_billing_period_tool",
      "agent_name": "csv_agent",
      "purpose": "Normalize billing periods"
    },
    {
      "tool_name": "compute_monthly_cost_tool",
      "agent_name": "cost_agent",
      "purpose": "Vercel Pro - convert monthly to monthly"
    },
    {
      "tool_name": "compute_monthly_cost_tool",
      "agent_name": "cost_agent",
      "purpose": "Vercel Pro - convert monthly to monthly"
    },
    {
      "tool_name": "compute_monthly_cost_tool",
      "agent_name": "cost_agent",
      "purpose": "Notion - convert yearly to monthly"
    },
    {
      "tool_name": "compute_monthly_cost_tool",
      "agent_name": "cost_agent",
      "purpose": "Notion - convert yearly to monthly"
    },
    {
      "tool_name": "compute_monthly_cost_tool",
      "agent_name": "cost_agent",
      "purpose": "Figma - convert quarterly to monthly"
    },
    {
      "tool_name": "compute_monthly_cost_tool",
      "agent_name": "cost_agent",
      "purpose": "Figma - convert quarterly to monthly"
    },
    {
      "tool_name": "compute_monthly_cost_tool",
      "agent_name": "cost_agent",
      "purpose": "AWS - convert monthly to monthly"
    },
    {
      "tool_name": "compute_monthly_cost_tool",
      "agent_name": "cost_agent",
      "purpose": "AWS - convert monthly to monthly"
    },
    {
      "tool_name": "compute_monthly_cost_tool",
      "agent_name": "cost_agent",
      "purpose": "Slack - convert yearly to monthly"
    },
    {
      "tool_name": "compute_monthly_cost_tool",
      "agent_name": "cost_agent",
      "purpose": "Slack - convert yearly to monthly"
    },
    {
      "tool_name": "compute_monthly_cost_tool",
      "agent_name": "cost_agent",
      "purpose": "Zoom - convert monthly to monthly"
    },
    {
      "tool_name": "compute_monthly_cost_tool",
      "agent_name": "cost_agent",
      "purpose": "Zoom - convert monthly to monthly"
    },
    {
      "tool_name": "compute_monthly_cost_tool",
      "agent_name": "cost_agent",
      "purpose": "GitHub - convert monthly to monthly"
    },
    {
      "tool_name": "compute_monthly_cost_tool",
      "agent_name": "cost_agent",
      "purpose": "GitHub - convert monthly to monthly"
    },
    {
      "tool_name": "compute_monthly_cost_tool",
      "agent_name": "cost_agent",
      "purpose": "Jira - convert quarterly to monthly"
    },
    {
      "tool_name": "compute_monthly_cost_tool",
      "agent_name": "cost_agent",
      "purpose": "Jira - convert quarterly to monthly"
    },
    {
      "tool_name": "compute_monthly_cost_tool",
      "agent_name": "cost_agent",
      "purpose": "HubSpot - convert yearly to monthly"
    },
    {
      "tool_name": "compute_monthly_cost_tool",
      "agent_name": "cost_agent",
      "purpose": "HubSpot - convert yearly to monthly"
    },
    {
      "tool_name": "compute_monthly_cost_tool",
      "agent_name": "cost_agent",
      "purpose": "Google Workspace - convert monthly to monthly"     
    },
    {
      "tool_name": "compute_monthly_cost_tool",
      "agent_name": "cost_agent",
      "purpose": "Google Workspace - convert monthly to monthly"     
    }
  ]
}
