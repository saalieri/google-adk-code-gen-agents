import os
from google.adk.tools.tool_context import ToolContext

def system(command: str) -> str:
    """Executes a system command and returns the output as a string."""
    print(f"--- Executing system command: {command} ---") # Log command execution
    result = os.popen(command).read()
    print(f"--- Command output: {result} ---") # Log command output
    return result

def write_code_to_file(code: str, filename: str) -> None:
    """Writes the given code to a file."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(code)

def exit_loop(tool_context: ToolContext):
    """Call this function ONLY when the critique indicates no further changes are needed, signaling the iterative process should end."""
    print(f"  [Tool Call] exit_loop triggered by {tool_context.agent_name}")
    tool_context.actions.escalate = True
    tool_context.actions.skip_summarization = True
    # Return empty dict as tools should typically return JSON-serializable output
    return ""