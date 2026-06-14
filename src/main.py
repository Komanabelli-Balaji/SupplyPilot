from tools.planning_tools import inventory_analysis

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

from negotiation import negotiate

observation = f"""
Inventory Analysis of product {product}:

{analysis}

Replenishment required.
"""

opinions = negotiate(observation)

for name, opinion in opinions.items():
    print()
    print(name.upper())
    print(opinion)


# response = planner.invoke(
#     {
#         "messages": [
#             {
#                 "role": "user",
#                 "content": content
#             }
#         ]
#     }
# )

# for msg in response["messages"]:
#     print(50*"-")
#     print(msg)

# print(50*"=")
# print(response["messages"][-1].content)
