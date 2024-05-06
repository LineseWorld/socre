import re


class Battle:
    """战役"""

    def __init__(self, record: dict, team_name: str):
        result = record["color"]
        if result == "win":
            self.result = 2
        elif result == "lose":
            self.result = 0
        else:
            self.result = 1

        score = str(record["score"])

        # 使用正则表达式匹配两个数字
        score_list = re.findall(r'\d+', score)

        team_a_score = score_list[0]
        team_b_score = score_list[1]

        team_a_name = record["team_A_name"]
        team_b_name = record["team_B_name"]

        if team_name == team_a_name:
            self.goal = team_a_score
            self.lose = team_b_score
        elif team_name == team_b_name:
            self.goal = team_b_score
            self.lose = team_a_score
        else:
            print("team_name %s is not find", team_name)



