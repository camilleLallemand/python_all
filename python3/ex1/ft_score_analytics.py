import sys


def score_analytics() -> None:
    if len(sys.argv) < 2:
        print(
            "No scores provided. Usage: python3 ft_score_analytics.py <score1> <score2> ...")
        return
    score = []
    for arg in sys.argv[1:]:
        try:
            score.append(float(arg))
        except ValueError:
            print(f"Invalid parameter: '{arg}'")
    if len(score) == 0:
        print(
            "No scores provided. Usage: python3 ft_score_analytics.py <score1> <score2> ...")
        return
    total_players = len(score)
    total_score = round(sum(score))
    average_score = total_score / total_players
    high_score = round(max(score))
    low_score = round(min(score))
    score_range = high_score - low_score

    print("Scores processed:", [round(i) for i in score])
    print("Total players:", total_players)
    print("Total score:", total_score)
    print("Average score:", average_score)
    print("High score:", high_score)
    print("Low score:", low_score)
    print("Score range:", score_range)


if __name__ == "__main__":
    print("=== Player Score Analytics ===")
    score_analytics()
