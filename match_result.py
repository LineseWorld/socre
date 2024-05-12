# 实现 对结果更新，在每次运行前处理
import re
from football_matches_database import DbMatchInfo


class MatchResult:
    def __init__(self, header_info):
        self.match_id = header_info["match_id"]
        self.team_a_name = header_info["team_A_name"]
        self.team_b_name = header_info["team_B_name"]
        self.status = header_info["status"]
        if self.status != "Played":
            return

        self.as_a = int(header_info["as_A"])
        self.as_b = int(header_info["as_B"])
        self.goal_num = self.as_a + self.as_b

        if self.as_a > self.as_b:
            self.result = "win"
        elif self.as_a == self.as_b:
            self.result = "draw"
        else:
            self.result = "loss"

        self.is_win = False
        self.is_goal_num = False
        self.is_score = False

    def check_prediction(self, prediction: DbMatchInfo):
        author_predict_win = prediction.author_predict_win
        author_predict_goal_num = prediction.author_predict_goal_num
        author_predict_score = prediction.author_predict_score
        self.is_win = (self.result == "win" and "胜" in author_predict_win) or (
                self.result == "draw" and "平" in author_predict_win) or (
                              self.result == "loss" and "负" in author_predict_win)

        match = re.search(r'(\d+)~(\d+)', author_predict_goal_num)

        if match:
            # 提取两个数字
            num1 = int(match.group(1))
            num2 = int(match.group(2))
            for i in range(num1, num2 + 1):
                if self.goal_num == i:
                    self.is_goal_num = True
                    break

        predict_score = self.extract_scores(author_predict_score)

        for score in predict_score:
            score1 = score[0]
            score2 = score[1]
            if score1 == self.as_a and score2 == self.as_b:
                self.is_score = True
                break

    def extract_scores(self, score_string):
        # 首先按“、”分割字符串
        scores_list = score_string.split('、')

        # 创建一个列表来存储解析后的比分
        parsed_scores = []

        # 遍历每个比分字符串
        for score in scores_list:
            # 使用正则表达式匹配比分格式（假设比分都是整数，且格式为“数字-数字”）
            match = re.match(r'(\d+)-(\d+)', score)
            if match:
                # 如果匹配成功，提取两个数字并添加到列表中
                parsed_scores.append((int(match.group(1)), int(match.group(2))))
            else:
                # 如果匹配失败，可以打印一个警告或采取其他措施
                print(f"Invalid score format: {score}")

        return parsed_scores
