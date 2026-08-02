from environment.runtime import set_env
from environment.scm_env import SupplyChainEnvironment
from graphs.scm_graph import graph
from simulation.logger import SimulationLogger

NUM_DAYS = 30

def simulate(output_file: str):

    env = SupplyChainEnvironment()
    set_env(env)

    logger = SimulationLogger()

    for day in range(1, NUM_DAYS + 1):

        state = {
            "env": env,
            "customer_demand": None,
            "customer_served": None,
            "rd_result": None,
            "df_result": None,
            "factory_plan": None,
            "metrics": None,
        }

        result = graph.invoke(state)

        logger.log_day(
            day,
            result["metrics"],
        )

        print(
            f"Day {day}/{NUM_DAYS} complete",
            end="\r",
        )

    logger.save(output_file)

    print()
    print("Simulation finished.")


if __name__ == "__main__":
    
    simulate("baseline.csv")