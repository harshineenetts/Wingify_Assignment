import os
from dotenv import load_dotenv
from crewai import Agent
from langchain_openai import ChatOpenAI

# Import the updated tools
from tools import search_tool, read_data_tool, analyze_investment_tool, create_risk_assessment_tool

load_dotenv()

### Loading LLM 
# Fix: Initialize an actual LLM instance instead of the recursive `llm = llm`
# Make sure you have OPENAI_API_KEY set in your .env file
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)

# Creating an Experienced Financial Analyst agent
financial_analyst = Agent(
    role="Senior Financial Analyst",
    goal="Accurately analyze financial documents and extract key metrics to answer the user's query: {query}",
    verbose=True,
    memory=True,
    backstory=(
        "You are a seasoned financial analyst with decades of experience examining corporate reports, "
        "10-Ks, and earnings updates. You rely strictly on provided data, perform accurate mathematical "
        "assessments, and provide grounded, objective financial insights. You never fabricate numbers."
    ),
    tools=[read_data_tool, search_tool], # Fix: changed `tool=` to `tools=`
    llm=llm,
    max_iter=3, # Fix: Increased from 1 so the agent actually has time to process
    allow_delegation=True
)

# Creating a document verifier agent
verifier = Agent(
    role="Financial Document Verifier",
    goal="Verify the contents of the uploaded file to ensure it is a valid financial document.",
    verbose=True,
    memory=True,
    backstory=(
        "You are a strict compliance officer. Your job is to read documents and quickly ascertain "
        "if they contain valid financial data, corporate earnings, or market reports. "
        "You ensure the team only works with legitimate, relevant financial files and reject anything else."
    ),
    tools=[read_data_tool],
    llm=llm,
    max_iter=2,
    allow_delegation=False
)

# Creating an investment advisor agent
investment_advisor = Agent(
    role="Investment Advisor",
    goal="Provide sound, risk-adjusted investment insights based on the financial document and analysis.",
    verbose=True,
    backstory=(
        "You are a fiduciary investment advisor. You base your recommendations strictly on "
        "fundamental analysis, market conditions, and verified financial data. You prioritize "
        "risk management over speculation and always provide actionable, evidence-based advice."
    ),
    tools=[analyze_investment_tool], 
    llm=llm,
    max_iter=3,
    allow_delegation=False
)

# Creating a risk assessor agent
risk_assessor = Agent(
    role="Risk Assessment Expert",
    goal="Identify and quantify potential market, operational, and financial risks from the document.",
    verbose=True,
    backstory=(
        "You are a meticulous risk manager. You look for supply chain vulnerabilities, "
        "margin compressions, macroeconomic headwinds, and regulatory risks within corporate filings. "
        "You provide clear, objective warnings without exaggerating."
    ),
    tools=[create_risk_assessment_tool],
    llm=llm,
    max_iter=3,
    allow_delegation=False
)