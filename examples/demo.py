import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import gambler

commands = [
    "new_game 12345",
    "status",
    "schedule",
    "news",
    "bet wnl 1 home 5000",
    "bet score 1 2-1 1000",
    "next",
    "status",
    "history",
]

for command in commands:
    print(f">>> {command}")
    print(gambler.cmd(command))
    print()
