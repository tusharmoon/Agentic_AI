import httpx
from pathlib import Path
from phi.agent import Agent
from phi.tools.csv_tools import CsvTools
from phi.model.mistral import MistralChat

from dotenv import load_dotenv
load_dotenv()

# ---------------------------
# Paths
# ---------------------------
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "wip"
DATA_DIR.mkdir(parents=True, exist_ok=True)

IMDB_CSV_PATH = DATA_DIR / "IMDB-Movie-Data.csv"

print("BASE_DIR : ",BASE_DIR)
print("DATA_DIR :",DATA_DIR)
print("IMDB_CSV_PATH",IMDB_CSV_PATH)

print("Stage 1 : BASE_DIR , DATA_DIR , IMDB_CSV_PATH Created and Added ......")

# ------------------------------
IMDB_URL = "https://phidata-public.s3.amazonaws.com/demo_data/IMDB-Movie-Data.csv"

if not IMDB_CSV_PATH.exists():
    print("Downloading IMDB dataset...")
    response = httpx.get(IMDB_URL)
    response.raise_for_status()
    IMDB_CSV_PATH.write_bytes(response.content)
else:
    print("IMDB dataset already exists.")
    
    
print("Stage 2 : If IMDB_CSV_PATH Added , Complete......")

# ------------------------------

# ---------------------------
# Create Agent
# DuckDbTools enable an Agent to run SQL and analyze data using DuckDb... This needs to install "uv add duckdb"
# ---------------------------
agent = Agent(
    name="IMDB CSV Assistant",
    role="Analyze IMDB movie data using CSV tools",
    model=MistralChat(model="mistral-small-latest"),
    tools=[CsvTools(csvs=[IMDB_CSV_PATH])],
    instructions=[
        "Always list available CSV files first",
        "Inspect columns before running queries",
        "Use CSV tools to answer questions accurately",
    ],
    markdown=True,
    show_tool_calls=True,
)

#print("Agent...",agent)
print("Stage 3 : CSV agent Configuration Complete......")

print("Stage 4 : Finally Running the agent using CLI......")

# ----------------------------

# ---------------------------
# Run CLI App
# ---------------------------
if __name__ == "__main__":
    agent.cli_app(stream=False)




