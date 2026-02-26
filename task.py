from crewai import Task

# Import all properly configured agents
from agents import financial_analyst, verifier, investment_advisor, risk_assessor

# Import the updated functional tools
from tools import search_tool, read_data_tool, analyze_investment_tool, create_risk_assessment_tool

## Creating a verification task
verification = Task(
    description=(
        "Review the document located at {file_path} using the read_data_tool. "
        "Verify if it is a legitimate corporate or financial report (e.g., earnings report, 10-K, etc.). "
        "If it is not a financial document, explicitly state that it is invalid."
    ),
    expected_output=(
        "A short confirmation stating whether the document at {file_path} is a valid financial report, "
        "along with a brief summary of what the document actually is."
    ),
    agent=verifier,
    tools=[read_data_tool],
    async_execution=False
)

## Creating a task to help solve user's query
analyze_financial_document = Task(
    description=(
        "Using the financial document located at {file_path}, thoroughly answer the user's specific query: '{query}'. "
        "Extract key financial metrics, revenue growth, operational highlights, and any other relevant data. "
        "Rely purely on the data provided in the text and do not hallucinate numbers."
    ),
    expected_output=(
        "A detailed, factual, and well-structured analysis of the financial document that directly answers the user's query. "
        "Include bullet points for key metrics and clear headings."
    ),
    agent=financial_analyst,
    tools=[read_data_tool, search_tool],
    async_execution=False,
)

## Creating a risk assessment task
risk_assessment = Task(
    description=(
        "Based on the data extracted from the document at {file_path}, identify the top business, "
        "operational, or market risks facing the company. "
        "Use the create_risk_assessment_tool to process the findings if needed. "
        "Be objective and highlight actual vulnerabilities mentioned or implied in the financials."
    ),
    expected_output=(
        "A structured risk assessment report highlighting potential vulnerabilities, market headwinds, "
        "and operational risks, supported by evidence from the document."
    ),
    agent=risk_assessor,
    tools=[read_data_tool, create_risk_assessment_tool],
    async_execution=False,
)

## Creating an investment analysis task
investment_analysis = Task(
    description=(
        "Review the financial analysis and risk assessment for the document at {file_path}. "
        "Provide a grounded investment outlook and address the user's query: '{query}'. "
        "Use the analyze_investment_tool to help synthesize the data. "
        "Provide actionable, evidence-based recommendations without reckless speculation."
    ),
    expected_output=(
        "A professional investment summary with clear reasoning based on the document's fundamentals. "
        "Include a final verdict (e.g., bullish, bearish, or neutral) with supporting arguments."
    ),
    agent=investment_advisor,
    tools=[read_data_tool, analyze_investment_tool],
    async_execution=False,
)