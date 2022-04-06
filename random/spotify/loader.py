from time import sleep
from rich.console import Console

console = Console()
tasks = [f"task {n}" for n in range(1, 11)]

with console.status("Working on tasks...", speed=2) as status:
    while tasks:
        task = tasks.pop(0)
        sleep(1)
        print(f"{task} complete")