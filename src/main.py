from agents.inventory_agent import agent

response = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content":
                "How many apples are available?"
            }
        ]
    }
)

print(response)
print(50*"-")
print(response["messages"][-1].content)