from graphs.inventory_graph import graph

config = {
    "configurable": {
        "thread_id": "inventory-thread"
    }
}

while True:
    query = input(">> ")

    if query == "exit":
        break

    result = graph.invoke({
            "messages": [(
                "user",
                query
            )]
        },
        config=config
    )

    for msg in result["messages"]:
        print(50*"-")
        print(msg)

    print(50*"=")
    print((result["messages"][-1].content)[0]["text"])
    # print((result["messages"][-1].content)[1]["text"])
