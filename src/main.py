from agents.inventory_agent import agent

response = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content":
                "We are getting low on milk."
            }
        ]
    }
)

for msg in response["messages"]:
    print(50*"-")
    print(msg)

print(50*"=")
print((response["messages"][-1].content)[0]["text"])
# print((response["messages"][-1].content)[1]["text"])