import subprocess


ALLOWED_COMMANDS = [
    "python",
    "dir",
    "type"
]


def run_command(command):

    command_parts = command.split()

    if command_parts[0] not in ALLOWED_COMMANDS:
        return {
            "success": False,
            "output": "Command not allowed."
        }

    try:

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            shell=True
        )

        output = result.stdout + result.stderr

        success = result.returncode == 0

        return {
            "success": success,
            "output": output if output else "Command executed successfully."
        }

    except Exception as e:

        return {
            "success": False,
            "output": str(e)
        }
