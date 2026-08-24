from src.agents.tools.calculator_tool import calculator
from src.agents.tools.datetime_tool import current_datetime
from src.agents.tools.weather_tool import weather
from src.agents.tools.web_search_tool import web_search


def get_tools() -> list:
    return [web_search, calculator, current_datetime, weather]
