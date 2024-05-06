from battle import Battle
import re


def ToStringWithBattle(results: []):
    result = ""
    win_count = 0
    draw_count = 0
    lose_count = 0

    for item in results:
        if item["result"] == "win":
            win_count += 1
        elif item["result"] == "draw":
            draw_count += 1
        else:
            lose_count += 1
    content = "近{}场交锋，胜{}，平{}，负{}。".format(len(results), win_count, draw_count, lose_count)
    if win_count + draw_count >= 4 and win_count >= 3:
        result = "对局大优"
    elif win_count > lose_count and draw_count <= 3:
        result = "对局小优"
    elif win_count == lose_count or draw_count >= 4:
        result = "势均力敌"
    elif lose_count + draw_count >= 4 and lose_count >= 3:
        result = "对局大劣"
    elif lose_count > win_count and draw_count <= 3:
        result = "对局小劣"

    if len(results) < 5:
        result = ""

    return content + result


def ToStringTeamLevel(rank: float) -> str:
    if 0 < rank < 5:
        return "上游球队"
    elif rank < 9:
        return "中上游球队"
    elif rank < 13:
        return "中下游球队"
    elif rank < 17:
        return "下游球队"
    else:
        return "保级球队"


def ToStringGameResult(results: []) -> str:
    result = ""
    lose = 0
    goal = 0
    result += "["
    count = 0
    for item in results:
        if item.result == 0:
            result += "x"
        elif item.result == 1:
            result += "-"
        else:
            result += "√"
        count += 1
        if len(results) != count:
            result += "、"
        lose += int(item.lose)
        goal += int(item.goal)
    result += "]"

    content = " 进球{}，失球{}:".format(goal, lose)

    if goal < 5:
        content += "进攻低迷，场均进球{}；".format(goal / 5.0)
    elif goal < 10:
        content += "进攻一般，场均进球{}；".format(goal / 5.0)
    else:
        content += "状态火热，场均进球{}；".format(goal / 5.0)

    if lose < 5:
        content += "防守较好，场均失球{}。".format(lose / 5.0)
    elif lose < 10:
        content += "防守一般，场均失球{}。".format(lose / 5.0)
    else:
        content += "防守较差，场均失球{}。".format(lose / 5.0)

    return result + content


def GetTeamLevel(ranks: []) -> float:
    """球队定档"""
    """
        根据ranks平均排名来区分
        在联赛中一般18~20支球队，中超16支
        1~4：上游球队
        5~8：中上游球队
        9~12：中下游球队
        13~16：下游球队
        17+: 保级球队
    """
    sum = 0.0
    for rank in ranks:
        if rank < 0:
            sum += 20 - rank

        else:
            sum += rank
    ava_rank = sum / len(ranks) * 1.0
    return ava_rank


class FootballTeam:
    """球队"""
    id = ""  # id
    name = ""  # 球队名
    recent_battles = []  # 近期战况
    recent_year_ranks = []  # 近几年联赛排名
    rank_str = ""  # 字符串排名
    current_rank = 0  # 当前排名
    win = 0  # 胜
    lose = 0  # 负
    tied = 0  # 平
    score = 0  # 分数
    goal_number = 0  # 进球数
    lose_goal_number = 0  # 失球数
    crew_status = "一般"  # 球员状态
    team_status = "一般"  # 球队状态
    win_rate = 0  # 总胜率-一期采用总胜率
    home_win_rate = 0  # 主场胜率 - 先不计算
    away_win_rate = 0  # 客场胜率 - 先不计算
    all_game_count = 0  # 总局数
    logo_url = ""  # 队标
    with_battle_history = []  # 交锋历史
    # 实力计算
    fight_spirit = 0  # 斗志
    team_level = 0  # 球队水平
    attack_ability = 0  # 进攻能力，进球数计算
    defence_ability = 0  # 防守能力，失球数计算
    general_ability = 0  # 综合能力

    def __init__(self, headerInfo: dict, analysisInitData: dict, teamType: str):

        league_table = dict()
        recent_record = dict()

        if teamType == "team_A":
            league_table = analysisInitData["league_table"]
            league_table = league_table["team_A"]
            recent_record = analysisInitData["recent_record"]
            recent_record = recent_record["team_A"]
        else:
            league_table = analysisInitData["league_table"]
            league_table = league_table["team_B"]
            recent_record = analysisInitData["recent_record"]
            recent_record = recent_record["team_B"]

        if teamType == "team_A":
            self.name = headerInfo["team_A_name"]
            self.rank_str = headerInfo["team_A_rank"]
            self.id = headerInfo["team_A_id"]
            self.logo_url = headerInfo["team_A_logo"]
        else:
            self.name = headerInfo["team_B_name"]
            self.rank_str = headerInfo["team_B_rank"]
            self.id = headerInfo["team_B_id"]
            self.logo_url = headerInfo["team_B_logo"]

        total_league = league_table["total"]
        self.win = int(total_league["matches_won"])
        self.lose = int(total_league["matches_lost"])
        self.tied = int(total_league["matches_draw"])
        self.current_rank = int(total_league["rank"])
        self.score = int(total_league["points"])
        self.win_rate = int(str(total_league["win_rate"]).replace("%", ""))
        self.goal_number = int(total_league["goals_pro"])
        self.lose_goal_number = int(total_league["goals_against"])
        self.all_game_count = int(total_league["matches_total"])
        home_league = league_table["home"]
        self.home_win_rate = int(str(home_league["win_rate"]).replace("%", ""))

        away_league = league_table["away"]
        self.away_win_rate = int(str(away_league["win_rate"]).replace("%", ""))

        self.recent_battles = []

        for record in recent_record:
            battle = Battle(record, self.name)
            self.recent_battles.append(battle)
            if len(self.recent_battles) >= 5:
                break

        battle_history = analysisInitData["battle_history"]
        battle_history = battle_history["list"]
        self.with_battle_history = []
        for battle in battle_history:
            battle_dict = dict()
            battle_dict["team_a_name"] = battle["team_A_name"]
            battle_dict["team_b_name"] = battle["team_B_name"]
            score = battle["score"]
            battle_dict["score"] = score
            match = re.search(r'(\d+)-(\d+)', score)
            if match:
                team_a_score = int(match.group(1))
                team_b_score = int(match.group(2))
                battle_dict["team_a_score"] = team_a_score
                battle_dict["team_b_score"] = team_b_score
                if battle_dict["team_a_name"] == self.name:
                    if team_a_score > team_b_score:
                        battle_dict["result"] = "win"
                    elif team_a_score == team_b_score:
                        battle_dict["result"] = "draw"
                    else:
                        battle_dict["result"] = "lose"
                else:
                    if team_b_score > team_a_score:
                        battle_dict["result"] = "win"
                    elif team_a_score == team_b_score:
                        battle_dict["result"] = "draw"
                    else:
                        battle_dict["result"] = "lose"
                self.with_battle_history.append(battle_dict)
            else:
                print("No match found.")

            if len(self.with_battle_history) >= 5:
                break

        sideline = analysisInitData["sideline"]
        crew_not_list = []
        if teamType == "team_A":
            crew_not_list = sideline["team_A"]
        else:
            crew_not_list = sideline["team_B"]

        self.crew_status = self.GetCrewStatus(crew_not_list)

        self.CalculateAbility()

    def SumRecentBattles(self) -> int:
        result = 0
        for battle in self.recent_battles:
            result += battle.result
        return result

    def CalculateAbility(self):
        """
        计算能力值

        :return:
        """
        self.score = self.win * 3 + self.tied
        self.all_game_count = self.win + self.tied + self.lose
        self.fight_spirit = 80  # todo 第一期默认都是80 范围0~100
        # todo 球队水平 不一定准确，需要同一级别联赛才准确
        # self.team_level = (20 - sum(self.recent_year_ranks) / 3.0) / 20.0 * 10

        if self.all_game_count == 0:
            self.attack_ability = 50
        else:
            # 进攻能力 = (实际进球率 + 0.01) / (5 + 0.01) × 100
            max_goal = 6
            adv_param = 0.01  # 调整值
            goal_rate = self.goal_number / self.all_game_count * 1.0
            self.attack_ability = (goal_rate + adv_param) / (max_goal + adv_param) * 100.0  # 范围0~100

        if self.all_game_count == 0:
            self.defence_ability = 50
        else:
            average_goals_conceded = self.lose_goal_number / self.all_game_count
            max_goals_conceded = 6  # 假设的最大场均失球数
            min_goals_conceded = 0.5  # 假设的最小场均失球数
            normalized_score = (max_goals_conceded - average_goals_conceded) / (
                    max_goals_conceded - min_goals_conceded) * 100
            self.defence_ability = round(normalized_score, 2)  # 保留两位小数

        # 综合能力值 = (近期五场比赛胜负情况得分 * 0.3) + (总比赛胜率得分 * 0.7)
        self.general_ability = self.SumRecentBattles()/5.0 * 50.0*0.3 + self.win_rate * 0.7

    def GetTeamContent(self) -> dict:
        result = dict()
        home_team_content_list = []
        content = "【{}】".format(self.name)
        result["name"] = self.name

        content = "【联赛情况】:排名{}，{}胜{}平{}负，积{}分, 胜率{}%".format(self.rank_str, self.win, self.tied, self.lose,
                                                                          self.score, self.win_rate)
        result["league_text"] = content

        content = "【近5场比赛】:{}".format(ToStringGameResult(self.recent_battles))
        result["recent_match_text"] = content

        content = "【球员情况】:{}".format(self.crew_status)
        result["crew_status_text"] = content

        content = "【球队情况】:{}".format(self.team_status)
        result["team_status_text"] = content

        result["team_logo_url"] = self.logo_url

        content = "【交锋历史】:{}".format(ToStringWithBattle(self.with_battle_history))
        result["recent_comp_text"] = content
        return result

    def GetCrewStatus(self, crew_not_list):
        size = len(crew_not_list)
        if size == 0:
            return "无人伤停，人员充足"
        elif size <= 4:
            return "伤停{}人，人员一般充足".format(size)
        else:
            return "伤停{}人，人员较为不足".format(size)
