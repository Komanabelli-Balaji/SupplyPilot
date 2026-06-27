from tools.scm_analysis import scm_analysis
from graphs.scm_graph import graph

metrics = scm_analysis()

retailer_state = {
    "inventory": metrics["inventory"],
    "daily_demand": 15,
    "reorder_point": metrics["reorder_point"],
    "eoq": metrics["eoq"]
}

distributor_state = {
    "inventory": metrics["distributor_inventory"],
    "safety_stock": metrics["distributor_safety_stock"],
    "lead_time": metrics["lead_time"]
}

factory_state = {
    "inventory": metrics["factory_inventory"],
    "capacity": metrics["production_capacity"]
}

result = graph.invoke(
    {
        "retailer_state": retailer_state,
        "distributor_state": distributor_state,
        "factory_state": factory_state,
    }
)

print()
print("RETAILER")
print(result["retailer_decision"])

print()
print("DISTRIBUTOR")
print(result["distributor_decision"])

print()
print("FACTORY")
print(result["factory_decision"])

print()
print("DISTRIBUTOR FINAL OFFER")
print(result["distributor_final_offer"])

print()
print("RETAILER REVIEW")
print(result["retailer_review"])

print()
print("FINAL")
print(result["final_decision"])