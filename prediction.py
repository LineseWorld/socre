import config
from competition import Competition
from football_team import FootballTeam
import math


def sigmoid(x):
    # Sigmoid函数，将任意实数映射到0到1之间
    return 1 / (1 + math.exp(-x))


def calculate_probabilities(team1_strength, team2_strength):
    # 计算实力差距
    strength_difference = team2_strength - team1_strength

    # 设定一个缩放因子，用于调整sigmoid函数的斜率
    scale_factor = 25.0  # 可以根据需要进行调整

    # 使用sigmoid函数计算胜、负、平的概率
    # 假设平局的概率在实力差距为0时最高，随着差距增大而减小
    draw_prob = sigmoid(-abs(strength_difference) / scale_factor)

    # 胜、负的概率是平局概率的补集，并且与实力差距的符号相关
    if strength_difference > 0:
        # 球队2胜的概率
        win_prob = (1 - draw_prob) / 2 * (1 + sigmoid(strength_difference / scale_factor))
        # 球队1负的概率
        loss_prob = 1 - win_prob - draw_prob
    else:
        # 球队1胜的概率
        win_prob = (1 - draw_prob) / 2 * (1 + sigmoid(-strength_difference / scale_factor))
        # 球队2负的概率
        loss_prob = 1 - win_prob - draw_prob

        # 验证概率之和是否为1（由于浮点数计算，可能会有轻微误差）
    assert abs(win_prob + loss_prob + draw_prob - 1.0) < 1e-6

    if team1_strength >= team2_strength:

        team1_win = max(win_prob, loss_prob)
        team1_loss = min(win_prob, loss_prob)

        return {
            'win': team1_win * 100.0,
            'loss': team1_loss * 100.0,
            'draw': draw_prob * 100.0
        }
    else:
        team1_win = min(win_prob, loss_prob)
        team1_loss = max(win_prob, loss_prob)

        return {
            'win': team1_win * 100.0,
            'loss': team1_loss * 100.0,
            'draw': draw_prob * 100.0
        }


class Prediction:

    def __init__(self, com: Competition):
        self.competition = com

    def GetWinNum(self, team: FootballTeam) -> float:
        """
        计算说明
        结果 = 斗志*斗志系数 + 进攻能力*进攻系数 + 防守能力*防守系数 + 综合能力*综合能力系数
        todo 斗志目前默认80、伤病为算进去
        进攻能力
        :param team:
        :return:
        """
        # print("team: ", team.fight_spirit, team.attack_ability, team.defence_ability, team.general_ability)
        return team.fight_spirit * config.FIGHT_SPIRIT_FACTOR + team.attack_ability * config.ATTACK_ABILITY_FACTOR + team.defence_ability * config.DEFENCE_ABILITY_FACTOR + team.general_ability * config.GENERAL_ABILITY_FACTOR

    def GetWinPrediction(self) -> dict:
        """
        home_win_num = GetWinNum + 主场胜率 * 主场胜率系数
        away_win_num = GetWinNum + 客场场胜率 * 客场胜率系数

        :return:
        """

        home_win_num = self.GetWinNum(
            self.competition.home_team) + self.competition.home_team.home_win_rate * config.HOME_AWAY_WIN_RATE_FACTOR
        away_win_num = self.GetWinNum(
            self.competition.away_team) + self.competition.away_team.away_win_rate * config.HOME_AWAY_WIN_RATE_FACTOR
        # print("home_win_num:", home_win_num)
        # print("away_win_num:", away_win_num)
        recommendations = calculate_probabilities(home_win_num, away_win_num)
        # print(recommendations)
        # advice_index = max(home_win_num, away_win_num) / (home_win_num + away_win_num)

        print("【大数据预测】 推荐指数： {}".format(recommendations))
        print("主队胜指数： %.2f, 客队胜指数 %.2f" % (home_win_num, away_win_num))

        return {
            "home_win_num": home_win_num,
            "away_win_num": away_win_num,
            "win": recommendations["win"],
            "loss": recommendations["loss"],
            "draw": recommendations["draw"],
        }

    def GetAttackIndex(self, team: FootballTeam) -> float:
        """
        进球指数 =  总进球数/总比赛场次 * 0.4 + 近期总进球数/近期比赛场次 * 0.6
        todo 后续完善 主客场区分
        :param team:
        :return:
        """
        sum_count = team.win + team.tied + team.lose
        ava_goal_number = 1
        if sum_count != 0:
            ava_goal_number = team.goal_number / sum_count * 1.0
        recent_goal_number = 0
        for battle in team.recent_battles:
            recent_goal_number += int(battle.goal)
        return (ava_goal_number * 0.4) + (recent_goal_number / len(team.recent_battles) * 1.0) * 0.6

    def GetLoseIndex(self, team: FootballTeam) -> float:
        """
        失球指数 = 总失球数/总比赛场次 * 0.4 + 近期总失球数/近期比赛场次 * 0.6
        todo 后续完善 主客场区分
        :param team:
        :return:
        """
        sum_count = team.win + team.tied + team.lose
        ava_lose_goal_number = 1
        if sum_count != 0:
            ava_lose_goal_number = team.lose_goal_number / sum_count * 1.0

        recent_lose_goal_number = 0
        for battle in team.recent_battles:
            recent_lose_goal_number += int(battle.lose)

        return ava_lose_goal_number * 0.4 + recent_lose_goal_number / len(team.recent_battles) * 0.6

    def GetAllGoalPrediction(self) -> []:
        """
        总进球数预测 =  (主队进球指数+客队失球指数)*0.5+(客队进球指数+主队失球指数)*0.5
        :return:
        """
        home_attack_index = self.GetAttackIndex(self.competition.home_team)
        home_lose_index = self.GetLoseIndex(self.competition.home_team)

        away_attack_index = self.GetAttackIndex(self.competition.away_team)
        away_lose_index = self.GetLoseIndex(self.competition.away_team)

        print("主队进球指数 %.2f, 失球指数 %.2f" % (home_attack_index, home_lose_index))

        print("客队进球指数 %.2f, 失球指数 %.2f" % (away_attack_index, away_lose_index))
        goal_result = (home_attack_index + away_lose_index) * 0.5 + (away_attack_index + home_lose_index) * 0.5
        print("预测进球数 %.2f " % goal_result)

        return home_attack_index, home_lose_index, away_attack_index, away_lose_index, goal_result

    def GetGoalPrediction(self) -> dict:
        result = dict()
        # return {
        #     "home_win_num":home_win_num,
        #     "away_win_num": away_win_num,
        #     "win": recommendations["win"],
        #     "loss": recommendations["loss"],
        #     "draw": recommendations["draw"],
        # }

        win_prediction = self.GetWinPrediction()
        result["home_win_index"] = str(round(win_prediction["home_win_num"], 2))
        result["away_win_index"] = str(round(win_prediction["away_win_num"], 2))
        result["win_advice_index"] = str(round(win_prediction["win"], 2))
        result["loss_advice_index"] = str(round(win_prediction["loss"], 2))
        result["draw_advice_index"] = str(round(win_prediction["draw"], 2))
        goal_prediction = self.GetAllGoalPrediction()
        all_goal = round(goal_prediction[4], 2)
        result["home_attack_index"] = str(round(goal_prediction[0], 2))
        result["home_lose_index"] = str(round(goal_prediction[1], 2))
        result["away_attack_index"] = str(round(goal_prediction[2], 2))
        result["away_lose_index"] = str(round(goal_prediction[3], 2))
        result["all_goal_index"] = all_goal
        # print(win_prediction)
        home_goal = all_goal * win_prediction["home_win_num"] / (
                win_prediction["home_win_num"] + win_prediction["away_win_num"])
        away_goal = all_goal * win_prediction["away_win_num"] / (
                win_prediction["home_win_num"] + win_prediction["away_win_num"])
        result["home_goal"] = str(round(home_goal, 2))
        result["away_goal"] = str(round(away_goal, 2))
        print("比分预测： %.2f-%.2f" % (home_goal, away_goal))
        # print(result)
        return result
