# Financial Document Analyzer - Debug Challenge Solution

## Project Overview
This project is a comprehensive financial document analysis system that processes corporate reports, financial statements, and investment documents using a sequential multi-agent system powered by CrewAI and FastAPI.

This repository contains the debugged and fully functional version of the original codebase, with critical architectural, logical, and prompt-engineering flaws resolved.

---

## Bug Hunt Report: What Was Fixed

The original codebase contained several intentional bugs across multiple layers of the application. Here is a detailed breakdown of the bugs identified and how they were resolved:

### 1. Sabotaged Prompts & Agent Personas (`agents.py` & `task.py`)
* **Bug:** The agents' goals and backstories contained "malicious" instructions telling them to hallucinate data, ignore compliance, act like Reddit day-traders, and make up fake URLs.
* **Fix:** Completely rewrote the prompts, roles, and backstories for the `financial_analyst`, `verifier`, `investment_advisor`, and `risk_assessor`. The agents are now strictly instructed to behave as fiduciary professionals, rely *only* on the provided data, and extract factual metrics.

### 2. Broken Tool Logic & Imports (`tools.py`)
* **Bug:** The `Pdf` class was used without being imported or existing as a standard library. `SerperDevTool` was imported incorrectly. The `InvestmentTool` and `RiskTool` were written as broken classes with infinite `while` loops and lacked proper CrewAI tool decorators.
* **Fix:** * Replaced the undefined `Pdf` loader with `PyPDFLoader` from `langchain_community`.
    * Corrected the `SerperDevTool` import.
    * Refactored all broken tool classes into standalone functions wrapped with the CrewAI `@tool` decorator, complete with strong type hinting and docstrings so the LLM knows how to use them.

### 3. Disconnected Data Flow & Context Injection (`main.py` & `task.py`)
* **Bug:** The FastAPI endpoint saved the uploaded PDF to a dynamic `file_path`, but this path was never passed into the CrewAI tasks. The agents had no idea where the document was located.
* **Fix:** Updated `financial_crew.kickoff()` in `main.py` to accept `inputs={'query': query, 'file_path': file_path}`. Updated task descriptions in `task.py` to use the `{file_path}` variable via string interpolation so the `read_data_tool` can access the file dynamically.

### 4. Incomplete Crew Execution (`main.py` & `task.py`)
* **Bug:** `main.py` only instantiated one agent (`financial_analyst`) and one task, completely ignoring the verifier, risk assessor, and investment advisor. Furthermore, all tasks in `task.py` were assigned to the `financial_analyst`.
* **Fix:** Correctly mapped tasks to their respective specialized agents in `task.py`. Assembled all four agents and tasks into the `Process.sequential` pipeline in `main.py`.

### 5. Application Crash Risks (`agents.py` & `requirements.txt`)
* **Bug:** `llm = llm` was recursively undefined in `agents.py`. The `requirements.txt` was missing critical dependencies (`python-multipart`, `pypdf`, `langchain-openai`, `uvicorn`) required to actually parse PDFs and run the FastAPI server.
* **Fix:** Initialized a proper `ChatOpenAI` LLM instance. Updated `requirements.txt` with all necessary packages. Fixed the uvicorn run command in `main.py` to use `"main:app"` to prevent multiprocessing reload issues.

---

## Setup and Usage Instructions

### 1. Prerequisites
* Python 3.10+
* An OpenAI API Key

### 2. Installation
Clone the repository and install the dependencies:
```sh
pip install -r requirements.txt