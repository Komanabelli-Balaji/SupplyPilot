from langchain.tools import tool

from environment.runtime import get_env


@tool
def get_current_demand() -> int:
    """
    Returns current customer demand.
    """
    env = get_env()
    return env.current_demand()


@tool
def get_forecast_demand() -> int:
    """
    Returns forecast demand.
    """
    env = get_env()
    return env.forecast_demand()