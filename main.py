# 实现输入参数，生成球队模板

import config
from football_team import FootballTeam
from competition import Competition
from battle import Battle
from prediction import Prediction
import spider
from draw3 import Poster
import download
from football_matches_database import FootballMatchesDatabase
import json
from datetime import datetime

if __name__ == '__main__':
    # 获取对阵基本信息

    game_id = input("输入比赛id：")
    g_game_detail = spider.GetGameDetail(game_id)

    # print(type(g_game_detail))
    header_info = spider.GetHeaderInfo(g_game_detail)

    analysis_init_data = spider.GetAnalysisInitData(g_game_detail)

    com1 = Competition(header_info, analysis_init_data)

    com_info = com1.GenerateTemplate()
    print(com_info["paper_title"])
    pre = Prediction(com1)
    # pre.GetWinPrediction()
    pre_info = pre.GetGoalPrediction()

    print("【笔者推荐】")
    author_info = dict()
    author_win = input("主队胜负推荐：")
    author_goal = input("进球数推荐：")
    author_score = input("比分推荐：")
    author_info["win_text"] = author_win
    author_info["goal_number_text"] = author_goal
    author_info["goal_text"] = author_score

    p = Poster()
    p.match_name = com_info["match_name"]
    p.match_time = com_info["match_time"]

    home_team = com_info["home_team"]
    p.team1_name = home_team["name"]
    p.team1_icon = "team1_icon.png"
    download.download_picture(home_team["team_logo_url"], "team1_icon.png")

    away_team = com_info["away_team"]
    p.team2_name = away_team["name"]
    p.team2_icon = "team2_icon.png"
    download.download_picture(away_team["team_logo_url"], "team2_icon.png")

    with FootballMatchesDatabase() as db:
        # 插入数据
        # 字符串日期时间
        date_string = com_info["match_time"]

        # 将字符串转换为datetime对象
        dt_object = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')

        # 将datetime对象转换为时间戳
        timestamp = dt_object.timestamp()
        match_data = {
            'match_id': game_id,
            'match_time': com_info["match_time"],
            'match_time_stamp': timestamp,
            'match_title': com_info["match_name"],
            'team_a_name': home_team["name"],
            'team_b_name': away_team["name"],
            'team_a_info': json.dumps(home_team,ensure_ascii=False),
            'team_b_info': json.dumps(away_team,ensure_ascii=False),
            'ai_predict_info': json.dumps(pre_info),
            'author_predict_win': author_win,
            'author_predict_goal_num': author_goal,
            'author_predict_score': author_score,
        }
        db.insert_or_replace_match(match_data)
        print("insert db success, data:[{}]".format(match_data))

    p.show(com_info, pre_info, author_info)
