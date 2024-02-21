import os
import subprocess


def run_command(command, get_output=False):
    """Run a shell command, optionally capturing its output."""
    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        shell=True,
        text=True,
    )
    if get_output:
        return result.stdout.strip()
    else:
        print(result.stdout)
        return result.returncode == 0


def find_python_files(directory):
    """Recursively find all Python files in the given directory."""
    python_files = []
    ignore_dirs = {".venv", ".github"}
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))
    return python_files


def get_python_files_to_check():
    """Get a list of modified and new Python files."""
    # Get modified files
    modified_files = run_command("git diff --name-only HEAD", get_output=True)
    # Get new (untracked) files
    new_files = run_command("git ls-files --others --exclude-standard", get_output=True)

    # Combine lists and filter for Python files
    all_files = set(modified_files.split("\n") + new_files.split("\n"))
    python_files = [file for file in all_files if file.endswith(".py")]

    return python_files


def main():
    # python_files = get_python_files_to_check()
    python_files = find_python_files("./")
    print(python_files)
    if not python_files:
        print("No Python files to check.")
        return

    files_to_check = " ".join(python_files)

    # Define your commands here, running them only on the detected Python files
    commands = [
        f"flake8 {files_to_check} --max-line-length 110",
        f"black {files_to_check} --check",
        f"isort {files_to_check} --check-only",
    ]

    for command in commands:
        print(f"Running: {command}")
        if not run_command(command):
            print(f"Command failed: {command}")
            if "black" in command or "isort" in command:
                fix_command = command.replace("--check", "").replace("--check-only", "")
                if input("Attempt auto-correction? (y/n): ").lower() == "y":
                    run_command(fix_command)


if __name__ == "__main__":
    main()
