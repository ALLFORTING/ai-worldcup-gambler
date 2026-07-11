import copy
import sys
from pathlib import Path


def configure_utf8_output():
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")


configure_utf8_output()

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import gambler


def assert_good(command, output):
    assert isinstance(output, str), f"{command!r} did not return a string"
    assert output.strip(), f"{command!r} returned empty output"
    assert "命令执行失败" not in output, f"{command!r} failed:\n{output}"


def normalized_implied_probability(match, pick):
    inverse = {key: 1 / value for key, value in match["odds"]["wnl"].items()}
    total = sum(inverse.values())
    return inverse[pick] / total


def wnl_rate(match, pick, runs=2000):
    wins = 0
    for index in range(runs):
        result = gambler._simulate_match(copy.deepcopy(match), gambler.RNG(index + 1000))
        if result["wnl"] == pick:
            wins += 1
    return wins / runs


def fixed_seed_true_positive_match():
    state = gambler._new_state(13)
    true_positive = next(
        signal
        for signal in state["round_news_signals"]
        if signal["category"] == "positive" and signal["true"] and signal["delta"] > 0
    )
    match = next(
        match
        for match in state["current_matches"]
        if true_positive["team_id"] in {match["home"], match["away"]}
    )
    pick = "home" if match["home"] == true_positive["team_id"] else "away"
    assert match["power_mods"][pick] == true_positive["delta"], (match, true_positive)
    assert match["probs"] == gambler._wnl_probs(match["home"], match["away"])
    return match, pick, true_positive


def main():
    state_one = gambler._new_state(24680)
    state_two = gambler._new_state(24680)
    assert state_one["news_signal_config"] == state_two["news_signal_config"]
    assert state_one["round_news_signals"] == state_two["round_news_signals"]
    assert state_one["round_power_mods"] == state_two["round_power_mods"]

    public_news = gambler._cmd_news(state_one)
    assert "round_news_signals" not in public_news
    assert "round_power_mods" not in public_news
    assert "true" not in public_news.lower()

    true_positive_match, pick, signal = fixed_seed_true_positive_match()
    noise_match = copy.deepcopy(true_positive_match)
    noise_match["power_mods"] = {"home": 0, "away": 0}

    implied_probability = normalized_implied_probability(true_positive_match, pick)
    noise_rate = wnl_rate(noise_match, pick)
    signal_rate = wnl_rate(true_positive_match, pick)

    assert signal["category"] == "positive" and signal["true"]
    assert signal_rate > implied_probability + 0.02, (signal_rate, implied_probability)
    assert signal_rate > noise_rate + 0.02, (signal_rate, noise_rate)
    assert abs(noise_rate - implied_probability) < 0.06, (noise_rate, implied_probability)

    print("News signal test passed.")


if __name__ == "__main__":
    main()
