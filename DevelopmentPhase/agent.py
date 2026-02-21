from google.adk.agents.llm_agent import LlmAgent
from google.adk.agents.loop_agent import LoopAgent
from InterpreterAgent.agent import InterpreterAgent
from CodeGenAgent.tools.writer import system, write_code_to_file, exit_loop as interpreter_exit_loop, exit_loop as qa_exit_loop
from CodeGenAgent.config.settings import MODEL

QualityAssuranceAgent = LlmAgent(
    model=MODEL,
    name='QualityAssuranceAgent',
    description='A quality assurance agent that checks research insights and quality of the generated code.',
    instruction="""
    You are QualityAssuranceAgent, and you are a quality assurance agent.
    
    **Research Insights:**
    {research_insights}

    **Original Code:**
    ```python
    {generated_code}

    DO NOT DO:
        - You are responsible for checking the quality of the generated code.
        - You are responsible for providing feedback to the ProgrammerAgent if there are any issues with the code and 
          if the code follows the research insights provided by LeetCodeResearcherAgent.

    Instructions:
        - You need to evaluate the cases based on the research insights provided by LeetCodeResearcherAgent.
        - Locate the directory path stored in {output_dir}. Use the `system` tool to create a file named "test_main.py" inside the {output_dir}. 
        - If {output_dir}/test_main.py already exists, you must overwrite its entire content with the new data.
        - Since it is a code block, you need to remove the triple backticks and the "python" language identifier before writing to the file.
        - Write the python code block to {output_dir}/test_main.py using `write_code_to_file` tool, it has 2 arguments.
            - The first argument is the code block without the triple backticks and the "python" language identifier.
            - The second argument is the filename, which should be "{output_dir}/test_main.py".
        - The python code should be indented properly in the file.
        - Do not rely on the ExecutorAgent tests results, you need to execute the test cases yourself to verify the correctness of the generated code.
        - Write a python test cases based on the research insights for QualityAssuranceAgent using `pytest`.
        - Execute a functional test using `.venv\Scripts\activate && pytest` using `system` tool.
        - If the test fails, provide feedback to the ProgrammerAgent what went wrong and what cases are failing, and ask ProgrammerAgent to generate a new code or fix it based on the feedback.
        - If the all test succeeds, call the `qa_exit_loop` function and return the test results as a string.
    """,
    tools=[system, write_code_to_file, qa_exit_loop],
    output_key="test_results"
)


DevelopmentPhase = LoopAgent(
    name='DevelopmentPhase',
    description='A development phase agent that orchestrates the workflow of InterpreterAgent and QualityAssuranceAgent to answer questions.',
    sub_agents=[InterpreterAgent, QualityAssuranceAgent],
    max_iterations=5,
)