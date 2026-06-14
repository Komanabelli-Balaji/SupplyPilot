from agents.planner import planner
from agents.procurement import procurement
from agents.finance import finance


def negotiate(observation):

    agents = {
        "planner": planner,
        "procurement": procurement,
        "finance": finance
    }

    opinions = {}

    for name, agent in agents.items():

        response = agent.invoke({
            "messages": [{
                "role": "user",
                "content": observation
            }]
        })

        opinions[name] = response["structured_response"]

    return opinions