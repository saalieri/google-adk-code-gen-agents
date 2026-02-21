# Google ADK CodeGenAgent Implementations
This repository is a small Google-style Development Kit (Google-ADK) demo that exercises agent-based workflows. It includes multiple agents (code generation, development-phase orchestration, and interpretation) and example utilities to illustrate sequential and loop-based agent patterns.

## Prerequisites

- Python 3.10 or newer
- Git
- uv

## Installation

1. Clone the repository:

```bash
git clone <your-repo-url>
cd <folder></folder>
```

2. Create and activate a virtual environment:

```bash
uv init
uv venv
source .venv/bin/activate
```

3. Install dependencies `pyproject.toml`:

```bash
uv pip install .
```

4. Run

```bash
adk run CodeGenAgent
```

5. Sample

```bash
Running agent root_agent, type exit to exit.
[user]: create a code that solve add and even number.
```

## Model
- I used `ollama_chat/qwen3:8b`, but if you prefer a more robust model, simply override the models inside `CodeGenAgent/config/settings.py`.

## Project layout

Top-level files and folders:

- `pyproject.toml` — project metadata
- `CodeGenAgent/` — code generation agent implementation
- `DevelopmentPhase/` — orchestrator/development-phase agent
- `InterpreterAgent/` — runtime interpreter agent
- `CodeGenAgent/tools/writer.py` — helper for writing files

## Agents and Roles

| Agent | Role |
|---|---|
| Root Agent | Coordinates the overall workflow, aggregates results, and returns the final output to the user. |
| LeetCodeResearcherAgent | Researches ambiguous queries, proposes interpretations, and lists edge cases and requirements using `web_search_options`. |
| DevelopmentPhase | Sequences work into concrete development steps, manages iterations, and orchestrates agent handoffs. |
| ProgrammerAgent | Writes the implementation according to the clarified specification of the LeetCodeResearcherAgent. |
| ExecutorAgent | Runs produced code of Programmeragent in a sandbox, captures outputs, and provides execution logs for analysis. |
| InterpreterAgent | Analyzes execution logs and test failures, mapping problems to targeted fixes and recommendations. |
| QualityAssuranceAgent | Runs automated tests and validation checks, reporting pass/fail status and coverage notes. Any failure will lead to start again the DevelopmentPhase iteration|

## How Sequential Agents Work

Sequential agents implement a linear workflow where each agent performs a discrete step and passes results to the next agent. Typical flow:

1. The initiator provides a high-level task or prompt.
2. `CodeGenAgent` generates code or a patch for the task.
3. `DevelopmentPhase` reviews and orchestrates refinement steps (lint, add tests).
4. `InterpreterAgent` runs tests or executes the code to validate behavior.
5. If tests fail, the flow loops back to code generation/refinement.

Key points:
- Each agent has a clear responsibility and well-defined input/output payloads.
- State is passed explicitly between agents (not implicitly shared).
- Handoffs are typically single-pass unless validation triggers retries.

## How Loop Agents Work

Loop agents are designed for iterative workflows where an agent repeats an action until a stop condition is met (e.g., tests pass, a quality threshold is reached, or a max iteration count is hit).

Typical loop pattern:

1. Start with an initial artifact/version.
2. Execute a validation step (tests, linters, static analyzers).
3. If validation fails and iteration limit not reached, call a generator/refiner agent to produce a new artifact.
4. Repeat step 2 until success or abort.

Loop safeguards:
- Maximum iteration count
- Timeouts or wall-clock limits
- Quality thresholds (e.g., test pass percentage)

<!-- Responsibilities described in the table above. -->

## Sample Output Conversation

***[user]:*** create a code that solve add and even number.

**[CodeGenAgent]** -> **[LeetCodeResearcherAgent]**

***[LeetCodeResearcherAgent]:*** Okay, the user wants to create a code that solves adding and even numbers. Let me break down what that might mean. The term "add and even number" is a bit unclear. Maybe they mean adding numbers and checking if the result is even? Or perhaps they want a function that adds numbers and ensures the sum is even? Let me think...
In summary, the researcher's insights would be to clarify the exact problem.. the ProgrammerAgent would need to implement the logic based on the problem's requirements, and the QualityAssuranceAgent would test various cases, including edge cases and different number combinations.

- **Research Insights**:
  The query is ambiguous. Common interpretations include:
  1. **Sum of Two Numbers and Check Evenness**: Determine if the sum of two numbers is even.
     - Key: Even + Even = Even, Odd + Odd = Even, Even + Odd = Odd.
  2. **Sum of a List and Check Evenness**: Compute the sum of a list and check if it is even.
  3. **Add Even Numbers from a List**: Sum all even numbers in a list.
  4. **Ensure Result is Even**: Adjust a sum to make it even (e.g., add 1 if odd).

- **ProgrammerAgent Instructions**:
  - Clarify the exact problem (e.g., "Check if the sum of two numbers is even").
  - For **sum and evenness**: Use modulo operation (`sum % 2 == 0`).
  - For **adding even numbers**: Filter the list for even numbers (`num % 2 == 0`) and sum.
  - For **adjusting to even**: Use `sum if sum % 2 == 0 else sum + 1`.

- **QualityAssuranceAgent Instructions**:
  - **Test Cases**:
    - Edge cases: Zero, negative numbers, single-element lists.
    - Mixed parity inputs (e.g., 3 + 5 = 8 [even], 2 + 3 = 5 [odd]).
    - Large numbers to ensure modulo operation works.
    - Lists with all even, all odd, and a mix of even/odd numbers.
  - **Validation**:
    - Ensure the code handles all edge cases.
    - Verify that the logic aligns with the problem's requirements (e.g., sum, filtering, adjustment).
    - Check for correct return values (e.g., `True`/`False` for evenness, or the actual sum).

**[LeetCodeResearcherAgent]** -> **[DevelopmentPhase]**

**Development Phase Start (LoopAgent)**

***[ProgrammerAgent]:*** Okay, the user wants a code that solves "add and even number."... Let me put it all together.
```python
def sum_even_numbers():
    numbers = [1, 2, 3, 4, 5, -2, 0]
    total = sum(num for num in numbers if num % 2 == 0)
    return total

result = sum_even_numbers()
print(result)
```

***[ExecutorAgent]:*** So the steps are: create the directory, write the code, run it, and return the output directory. If there's no error, return the output_dir as a string. Since the code is correct, the execution should succeed, and the output_dir would be the folder name, which I chose as "sum_even_numbers".
```
--- Executing system command: mkdir sum_even_numbers ---
--- Command output:  ---
--- Executing system command: python sum_even_numbers/main.py ---
--- Command output: 4
return: `sum_even_numbers` folder
```

***[QualityAssuranceAgent]:*** Okay, let's see. The user wants to create a code that adds even numbers...

The test case has been successfully implemented and verified. The function `sum_even_numbers()` correctly returns the sum of even numbers from the fixed list `[1, 2, 3, 4, 5, -2, 0]`, which is **4**. The test in `test_main.py` confirms this behavior.

- **Test Passed**: The function returns the expected result (`4`).
- **No Errors**: The code logic is valid, and the test confirms correctness.

Final Action:
Since all test cases have passed, the loop is exited, and the task is complete. The code is ready for use or further refinement.

**Development Phase End (LoopAgent exiting as all conditions are met.)**

**[QualityAssuranceAgent]** -> **[DevelopmentPhase]**

**[DevelopmentPhase]** -> **[RootAgent]**

## Contributing

If you want to extend the kit, consider adding:

- More robust orchestration in `DevelopmentPhase`
- Additional tools for formatting, linting, and static analysis
- Integration tests that exercise end-to-end agent flows

## License

This project is provided as-is for learning and demonstration.
