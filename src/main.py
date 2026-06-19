import json

from tools.scm_analysis import scm_analysis
from graphs.scm_graph import graph

metrics = scm_analysis()

result = graph.invoke(
    {
        "metrics": metrics
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
print("FINAL")
print(result["final_decision"])