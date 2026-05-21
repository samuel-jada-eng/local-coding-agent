from ollama import chat
from rich.console import Console
from tools.file_tools import read_file, write_file, list_files
from tools.terminal_tools import run_command
import json
from memory.project_index import scan_project
from memory.vector_store import search_memory

console = Console()

SYSTEM_PROMPT = """
You are a coding agent with access to tools.

AVAILABLE TOOLS:

1. read_file(filepath)
2. write_file(filepath, content)
3. list_files(directory)
4. run_command(command)
5. scan_project(directory)
6. search_memory(query)

When using a tool, respond ONLY with valid JSON.

Examples:

{
  "tool": "run_command",
  "args": {
    "command": "python --version"
  }
}

{
  "tool": "read_file",
  "args": {
    "filepath": "main.py"
  }
}

{
  "tool": "write_file",
  "args": {
    "filepath": "hello.py",
    "content": "print('hello')"
  }
}
{
  "tool": "scan_project",
  "args": {
    "directory": "."
  }
}
{
  "tool": "search_memory",
  "args": {
    "query": "authentication logic"
  }
}
If no tool is needed, respond normally.

DO NOT wrap JSON in markdown.
DO NOT explain tool usage.
ONLY output raw JSON when calling tools.
"""

messages = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
]

console.print("[bold green]Coding Agent Started[/bold green]")

while True:
    user_input = input("\nYou: ")

    if user_input.lower() in ["exit", "quit"]:
        break

    messages.append({
        "role": "user",
        "content": user_input
    })

    response = chat(
        model="qwen2.5-coder:3b",
        messages=messages,
        options={"temperature": 0}
    )

    assistant_reply = response["message"]["content"]

    MAX_ITERATIONS = 5

    current_response = assistant_reply

    for _ in range(MAX_ITERATIONS):

        try:
            tool_data = json.loads(current_response)

            tool_name = tool_data["tool"]
            args = tool_data["args"]

            console.print(f"\n[bold yellow]Using Tool:[/bold yellow] {tool_name}")

            if tool_name == "read_file":
                result = read_file(args["filepath"])

            elif tool_name == "write_file":
                result = write_file(
                    args["filepath"],
                    args["content"]
                )

            elif tool_name == "list_files":
                result = list_files(
                    args["directory"]
                )

            elif tool_name == "run_command":
                result = run_command(
                    args["command"]
                )

            elif tool_name == "scan_project":
                result = scan_project(
                    args["directory"]
                )

            elif tool_name == "search_memory":
                result = search_memory(
                    args["query"]
                )

            else:
                result = "Unknown tool."

            console.print("\n[bold cyan]Tool Result:[/bold cyan]")
            print(result)

            messages.append({
                "role": "assistant",
                "content": current_response
            })

            messages.append({
               "role": "user",
               "content": f"""
           Tool result:
           {result}

           IMPORTANT:
           - If the command failed, analyze the error carefully.
           - Fix the issue using tools if possible.
           - Retry execution after fixing.
           - Continue until the task succeeds or you cannot continue.

           Use tools when necessary.
           """
            })

            next_response = chat(
                model="qwen2.5-coder:3b",
                messages=messages,
                options={
                    "temperature": 0
                }
            )

            current_response = next_response["message"]["content"]

        except json.JSONDecodeError:

            console.print(f"\n[bold green]Agent:[/bold green] {current_response}")

            messages.append({
                "role": "assistant",
                "content": current_response
            })

            break
