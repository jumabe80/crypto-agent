import os
from dotenv import load_dotenv
from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI

# Load your API key from .env file
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# ---- TOOL 1: Get Funding Rates (mocked data) ----
def get_funding_rates(_: str = "") -> str:
    rates = {
        "BTC-USDT": 0.031,
        "ETH-USDT": -0.015,
        "ARB-USDT": 0.082,
        "DOGE-USDT": 0.005
    }
    return "\n".join([f"{k}: {v}%" for k, v in rates.items()])

# ---- TOOL 2: Calculate Arbitrage ----
def calculate_arbitrage(_: str = "") -> str:
    rates = {
        "BTC-USDT": 0.031,
        "ETH-USDT": -0.015,
        "ARB-USDT": 0.082,
        "DOGE-USDT": 0.005
    }
    threshold = 0.03
    opportunities = [k for k, v in rates.items() if abs(v) > threshold]
    if opportunities:
        return f"🟢 Arbitrage opportunities found: {', '.join(opportunities)}"
    else:
        return "🔴 No arbitrage opportunities above 0.03% funding rate"

# ---- DEFINE LANGCHAIN TOOLS ----
tools = [
    Tool.from_function(
        func=get_funding_rates,
        name="GetFundingRates",
        description="Use this to get current funding rates for crypto perpetual pairs"
    ),
    Tool.from_function(
        func=calculate_arbitrage,
        name="EvaluateArbitrage",
        description="Use this to check if there's any arbitrage opportunity based on funding rates"
    )
]

# ---- SETUP LLM & AGENT ----
llm = OpenAI(temperature=0, openai_api_key=openai_api_key)

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent="zero-shot-react-description",
    verbose=True
)

# ---- RUN AGENT ----
query = "Check crypto funding rates and tell me if there's any arbitrage opportunity."
response = agent.run(query)

print("\n👉 Result:", response)
