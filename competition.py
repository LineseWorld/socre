import config
from football_team import FootballTeam


class Competition:
    """比赛"""
    id = ""  # 比赛id
    name = ""  # 比赛名称
    round_number = ""  # 轮次
    date = ""  # 比赛日期 yyyy-mm-dd
    start_play = ""  # 比赛时间 hh:mm

    def __init__(self, header_info: dict, analysis_init_data: dict):
        self.id = header_info["match_id"]
        self.name = header_info["competition_name"]  # 比赛名称
        self.round_number = header_info["gameweek"]  # 轮次
        self.date = header_info["date_utc"]  # 比赛日期 yyyy-mm-dd
        self.start_play = header_info["start_play"]  # 比赛时间 yyyy-mm-dd hh:mm

        self.home_team = FootballTeam(header_info, analysis_init_data, "team_A")  # 主队
        self.away_team = FootballTeam(header_info, analysis_init_data, "team_B")  # 客队

    def GetGaolNumberPrediction(self) -> float:
        home_predict_goal = self.home_team.goal_number / 100.0
        return home_predict_goal

    def GenerateTemplate(self) -> dict:
        result = dict()
        title = ""
        if len(self.round_number) == 0:
            title = "【竞猜】%s %s vs %s" % (
                self.name, self.home_team.name, self.away_team.name)  # xx 第 n 轮 xxx vs yyy
            result["match_name"] = self.name
        else:
            title = "【竞猜】%s 第%s轮 %s vs %s" % (
                self.name, self.round_number, self.home_team.name, self.away_team.name)  # xx 第 n 轮 xxx vs yyy
            result["match_name"] = "{} 第{}轮".format(self.name, self.round_number)

        result["paper_title"] = title
        result["match_time"] = self.start_play
        ht_content = self.home_team.GetTeamContent()
        result["home_team"] = ht_content
        at_content = self.away_team.GetTeamContent()
        result["away_team"] = at_content
        print(result)

        return result
