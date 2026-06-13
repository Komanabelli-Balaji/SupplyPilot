# from graphs.inventory_graph import graph

# config = {
#     "configurable": {
#         "thread_id": "inventory-thread"
#     }
# }

# while True:
#     query = input(">> ")

#     if query == "exit":
#         break

#     result = graph.invoke({
#             "messages": [(
#                 "user",
#                 query
#             )]
#         },
#         config=config
#     )

#     for msg in result["messages"]:
#         print(50*"-")
#         print(msg)

#     print(50*"=")
#     print((result["messages"][-1].content)[0]["text"])
#     # print((result["messages"][-1].content)[1]["text"])

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

from agents.planner import planner

content = f"""
Inventory Analysis object of product {product} is as follows:
{analysis}
Replenishment has already been determined to be necessary.
Recommend an order quantity.
"""

response = planner.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": content
            }
        ]
    }
)

for msg in response["messages"]:
    print(50*"-")
    print(msg)

print(50*"=")
print(response["messages"][-1].content)
