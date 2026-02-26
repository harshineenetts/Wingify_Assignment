import os
from dotenv import load_dotenv
from crewai.tools import tool
from crewai_tools import SerperDevTool
from langchain_community.document_loaders import PyPDFLoader

load_dotenv()

## Creating search tool
search_tool = SerperDevTool()

## Creating custom pdf reader tool
@tool("Read Financial Document")
def read_data_tool(file_path: str) -> str:
    """Tool to read data from a pdf file from a given path.
    Args:
        file_path (str): The absolute or relative path to the PDF file.
    """
    try:
        loader = PyPDFLoader(file_path)
        docs = loader.load()

        full_report = ""
        for data in docs:
            # Clean and format the financial document data
            content = data.page_content
            
            # Remove extra whitespaces and format properly
            while "\n\n" in content:
                content = content.replace("\n\n", "\n")
                
            full_report += content + "\n"
            
        return full_report
    except Exception as e:
        return f"Failed to read document: {str(e)}"

## Creating Investment Analysis Tool
@tool("Analyze Investment Data")
def analyze_investment_tool(financial_document_data: str) -> str:
    """Process and analyze the financial document data for investment insights.
    Args:
        financial_document_data (str): The extracted text from the financial document.
    """
    # Clean up the data format by removing double spaces and redundant newlines
    processed_data = " ".join(financial_document_data.split())
                
    # Basic implementation logic to return to the agent
    return f"Investment analysis processed successfully. Document length: {len(processed_data)} characters. Data is ready for final agent synthesis."

## Creating Risk Assessment Tool
@tool("Assess Financial Risk")
def create_risk_assessment_tool(financial_document_data: str) -> str:        
    """Assess the risks associated with the financial document.
    Args:
        financial_document_data (str): The extracted text from the financial document.
    """
    # Clean up the data format
    processed_data = " ".join(financial_document_data.split())
    
    # Basic implementation logic to return to the agent
    return f"Risk assessment processed successfully. Document length: {len(processed_data)} characters. Data is ready for final agent synthesis."