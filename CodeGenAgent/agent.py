from google.adk.agents.llm_agent import LlmAgent
from google.adk.agents.sequential_agent import SequentialAgent
from DevelopmentPhase.agent import DevelopmentPhase
from CodeGenAgent.config.settings import SEARCH_MODEL


LeetCodeResearcherAgent = LlmAgent(
    model=SEARCH_MODEL,
    name='LeetCodeResearcherAgent',
    description='A leetcode researcher that researches leetcode questions and provides insights.',
    instruction="""
    You are LeetCodeResearcherAgent, and you are a leetcode researcher primarily use `python` to research leetcode questions.

    Instructions:
        - Research the question and provide insights that can help answer the question.
        - Do not provide any code, only provide insights that can help answer the question.
        - The insights should be based on the question and should be relevant to the question.
        - Use the `google_search` tool to research the question and provide insights based on the search results.
        - Provide instructions for the `ProgrammerAgent` to answer the question based on the insights you provided. 
        - It should contain the simulation of how the `ProgrammerAgent` should think and approach the problem, 
          it should not be a direct answer to the question but rather a guide for the `ProgrammerAgent` to come up with the answer.
        - Provide instructions for the `QualityAssuranceAgent` to check the quality of the generated code and the execution result.
        - It should contain all the cases that the `QualityAssuranceAgent` should consider for creating test cases.
        - The instructions for `QualityAssuranceAgent` and `ProgrammerAgent` should be in bullet points and should be clear and concise.
    """,
    output_key="research_insights"
)

root_agent = SequentialAgent(
    name='root_agent',
    description='A root_agent orchestrates the workflow of LeetCodeResearcherAgent and DevelopmentPhase to answer questions.',
    sub_agents=[LeetCodeResearcherAgent, DevelopmentPhase]
)
