from google.adk.agents.llm_agent import LlmAgent
from google.adk.agents.sequential_agent import SequentialAgent
from CodeGenAgent.tools.writer import system, write_code_to_file, exit_loop as interpreter_exit_loop, exit_loop as qa_exit_loop
from CodeGenAgent.config.settings import MODEL

ProgrammerAgent = LlmAgent(
    model=MODEL,
    name='ProgrammerAgent',
    description='A python programmer that interprets the insights from LeetCodeResearcherAgent and generates python code.',
    instruction="""
    You are ProgrammerAgent, and you are a python programmer. 
    You will be given insights from LeetCodeResearcherAgent, and you will generate python code based on those insights and simulations.

    **Insights from LeetCodeResearcherAgent:**
    {research_insights}

    Instructions:
        - You need to evaluate the cases based on the research insights provided by LeetCodeResearcherAgent or feedback from the QualityAssuranceAgent.
        - Write a complete python code block that answers the question based on the insights and simulations for ProgrammerAgent.
        - The code should not include user input just create default variables for the input.
        - The code should not include test cases for the code, you are only responsible for generating the code based on the insights and simulations provided by LeetCodeResearcherAgent.
        - The code block should be executable and should not require any additional code to run.
        - The code block should be enclosed in triple backticks (```python ... ```).
        - Do not include any explanations or comments in the code block, only the code.
    """,
    output_key="generated_code"
)

ExecutorAgent = LlmAgent(
    model=MODEL,
    name='ExecutorAgent',
    description='A python code executor that executes python code and returns the output.',
    instruction="""
    You are ExecutorAgent, and you are a python code executor using `system` tool meaning you are writing actual folder and python files. 
    You will be given a python code block and use the `system` tool to execute the command.
    The input will be in the format of a complete Python code block, enclosed in triple backticks (```python ... ```).

    **Original Code:**
    ```python
    {generated_code}
    ```

    Instructions:
        - Make new folder related to the python code using `mkdir` command using `system` tool and store the folder name in output_dir.
        - Create new file main.py in the directory using `system` tool, if the file is already there, overwrite it.
        - Since it is a code block, you need to remove the triple backticks and the "python" language identifier before writing to the file.
        - Write the python code block to main.py using `write_code_to_file` tool, it has 2 arguments.
            - The first argument is the code block without the triple backticks and the "python" language identifier.
            - The second argument is the filename, which should be "main.py" and it should be in the new directory you created.
        - The python code should be indented properly in the file.
        - Execute main.py using `python main.py` using `system` tool.
        - If it requires user input, use `echo` command to provide the input and pipe it to the `python main.py` command.
        - If the code execution results in an error, provide the error message as feedback to the QualityAssuranceAgent.
        - If the code execution results is success return output_dir as a string.

    """,
    tools=[system, write_code_to_file],
    output_key="output_dir"
)

InterpreterAgent = SequentialAgent(
    name='InterpreterAgent',
    description='A interpreter agent that orchestrates the workflow of ProgrammerAgent and ExecutorAgent to execute the python code.',
    sub_agents=[ProgrammerAgent, ExecutorAgent],
)
