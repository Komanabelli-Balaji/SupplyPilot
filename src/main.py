import json

from tools.planning_tools import inventory_analysis
from graphs.negotiation_graph import graph

product = input("Enter product name: ")

analysis = inventory_analysis.invoke(
    {
        "product": product
    }
)

print(analysis)

if not (
    analysis["inventory"]
    < analysis["reorder_point"]
):
    print("WAIT")
    exit()

observation = json.dumps(
    analysis,
    indent=2
)

result = graph.invoke(
    {
        "observation": observation
    }
)

print()
print("PLANNER")
print(result["planner_opinion"])

print()
print("PROCUREMENT")
print(result["procurement_opinion"])

print()
print("FINANCE")
print(result["finance_opinion"])

print()
print("FINAL DECISION")
print(result["final_decision"])