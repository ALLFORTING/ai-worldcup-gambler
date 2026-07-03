import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import gambler


SEED = 20260703


def money_from_status(status_text):
    match = re.search(r"现金：([0-9,]+)", status_text)
    if not match:
        return 0
    return int(match.group(1).replace(",", ""))


def status_brief(status_text):
    interesting = ("现金：", "债务：", "净资产：", "当前轮次：", "阶段：", "称号：", "累计盈亏：")
    return "\n".join(line for line in status_text.splitlines() if line.startswith(interesting))


def parse_schedule(schedule_text):
    matches = []
    current = None
    for line in schedule_text.splitlines():
        match_line = re.match(r"^\[(\d+)\]\s+(.+)$", line)
        if match_line:
            current = {"index": int(match_line.group(1)), "pick": "home", "has_pk": False}
            matches.append(current)
            continue

        if current and "胜平负：" in line:
            odds = re.findall(r"\b(home|draw|away)\s+([0-9]+(?:\.[0-9]+)?)", line)
            if odds:
                current["pick"] = min(((float(value), pick) for pick, value in odds))[1]

        if current and "点球大战：" in line:
            current["has_pk"] = True
    return matches


def print_command(command):
    print(f">>> {command}")
    output = gambler.cmd(command)
    print(output)
    print()
    return output


def main():
    print("=" * 72)
    print("AI World Cup Gambler · full demo")
    print("This is a virtual simulator. No real money, no real betting advice.")
    print("=" * 72)
    print_command(f"new_game {SEED}")

    for round_no in range(1, 18):
        print("=" * 72)
        print(f"ROUND {round_no}")
        print("=" * 72)

        status = gambler.cmd("status")
        print(">>> status (brief)")
        print(status_brief(status))
        print()

        schedule = print_command("schedule")
        print_command("news")

        matches = parse_schedule(schedule)
        for match in matches:
            status = gambler.cmd("status")
            cash = money_from_status(status)
            if cash <= 0:
                print_command("loan")
                status = gambler.cmd("status")
                cash = money_from_status(status)

            if cash >= 100:
                amount = 1000 if cash >= 1000 else 100
                print_command(f"bet wnl {match['index']} {match['pick']} {amount}")
            else:
                print(f"Skip match {match['index']}: cash is below minimum bet.")
                print()
                continue

            status = gambler.cmd("status")
            cash = money_from_status(status)
            if match["has_pk"] and cash >= 500:
                print_command(f"bet pk {match['index']} no 500")

        next_output = print_command("next")
        if "游戏已结束" in next_output or "世界杯结束" in next_output:
            break

    print("=" * 72)
    print("FINAL SNAPSHOT")
    print("=" * 72)
    for command in ["status", "standings", "titles", "history", "quit"]:
        print_command(command)


if __name__ == "__main__":
    main()
