from langchain.tools import tool

from environment.runtime import get_env


@tool
def get_regular_capacity() -> int:
    """
    Returns factory regular production capacity.
    """
    env = get_env()
    return env.capacity()["regular_production"]


@tool
def get_overtime_capacity() -> int:
    """
    Returns factory overtime production capacity.
    """
    env = get_env()
    return env.capacity()["overtime_production"]