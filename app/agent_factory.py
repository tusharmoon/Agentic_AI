from pathlib import Path
from phi.agent import Agent
from phi.tools.csv_tools import CsvTools
from phi.model.mistral import MistralChat


def create_csv_agent(csv_path: Path) -> Agent:
    """
    Creates a CSV agent dynamically for any uploaded CSV file
    """

    return Agent(
        name="CSV Analysis Assistant",
        role="Analyze user-uploaded CSV files and answer questions",
        model=MistralChat(model="mistral-small-latest"),
        tools=[CsvTools(csvs=[csv_path])],
        instructions=[
            "Always list the available CSV files",
            "Inspect column names before querying",
            "Use CSV tools to answer questions accurately",
            "If a column is unclear, ask the user for clarification",
        ],
        markdown=True,
        show_tool_calls=True,
    )
