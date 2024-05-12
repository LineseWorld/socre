# 单元测试 程序
from draw3 import Poster
import config
from football_team import FootballTeam
from competition import Competition
from battle import Battle
from prediction import Prediction
import spider
from draw3 import Poster
import download
from prediction import calculate_probabilities
from match_result import MatchResult
from football_matches_database import FootballMatchesDatabase,DbMatchInfo
from dqd_crawler import *
import contextlib
def test_draw():
    print("test_draw")

    com_info = dict()
    pre_info = dict()
    author_info = dict()
    com_home_team = dict()
    com_away_team = dict()

    com_info["match_name"] = "欧洲杯"
    com_info["match_time"] = "2024-05-05 20:00:00"

    com_home_team["name"] = "西班牙"
    com_home_team["league_text"] = "【联赛情况】: 排名西甲第13，10胜7平15负，积37分, 胜率32%"
    com_home_team["recent_match_text"] = "【近5场比赛】:[√、x、-、x、-] 进球1，失球8；进攻低迷，场均进球0.2。防守一般，场均失球1.6"
    com_home_team["recent_comp_text"] = "【交锋历史】:近5场交锋，胜2，平1，负2。势均力敌"
    com_home_team["crew_status_text"] = "【球员情况】:伤病4、停赛3。主力球员伤停较多"
    com_home_team["team_status_text"] = "【球队状态】:1111"

    com_away_team["name"] = "西班牙"
    com_away_team["league_text"] = "【联赛情况】: 排名西甲第13，10胜7平15负，积37分, 胜率32%"
    com_away_team["recent_match_text"] = "【近5场比赛】:平、负、负、负、平、近五场，进球1，失球8:进攻低迷，场均进球0.2;防守一般，场均失球1.6"
    com_away_team["recent_comp_text"] = "【交锋历史】:近5场交锋，胜2，平1，负2。势均力敌"
    com_away_team["crew_status_text"] = "【球员状态】:伤病4、停赛3"
    com_away_team["team_status_text"] = "【球队状态】:1111"

    com_info["home_team"] = com_home_team
    com_info["away_team"] = com_away_team

    # 算法预测
    pre_info["win_advice_index"] = "11.00"
    pre_info["loss_advice_index"] = "12.00"
    pre_info["draw_advice_index"] = "89.00"
    pre_info["advice_index"] = "68.8"
    pre_info["home_win_index"] = "100"
    pre_info["away_win_index"] = "50"
    pre_info["home_attack_index"] = "3.1"
    pre_info["home_lose_index"] = "0.5"

    pre_info["away_attack_index"] = "2.1"
    pre_info["away_lose_index"] = "1.89"

    pre_info["all_goal_index"] = "3.72"
    pre_info["home_goal"] = "2.43"
    pre_info["away_goal"] = "1.54"

    # 笔者预测
    author_info["win_text"] = "胜、负、平"
    author_info["goal_number_text"] = "2~3"
    author_info["goal_text"] = "2-1、2-0、3-1"

    p = Poster()
    p.match_name = com_info["match_name"]
    p.match_time = com_info["match_time"]

    home_team = com_info["home_team"]
    p.team1_name = home_team["name"]
    p.team1_icon = "team1_icon.png"

    away_team = com_info["away_team"]
    p.team2_name = away_team["name"]
    p.team2_icon = "team2_icon.png"

    p.show(com_info, pre_info, author_info)


# test_draw()

def test_predict():
    game_id = "53637115"
    g_game_detail = spider.GetGameDetail(game_id)

    # print(type(g_game_detail))
    header_info = spider.GetHeaderInfo(g_game_detail)

    analysis_init_data = spider.GetAnalysisInitData(g_game_detail)

    com1 = Competition(header_info, analysis_init_data)

    com_info = com1.GenerateTemplate()

    pre = Prediction(com1)
    # pre.GetWinPrediction()
    pre_info = pre.GetGoalPrediction()


# test_predict()

def test_calculate_probabilities():
    # print(calculate_probabilities (33.54, 73.81))
    #
    # print(calculate_probabilities(73.81, 33.54))
    # print(calculate_probabilities(60, 40))
    for i in range(1, 100):
        print("team1: {} , team2 :{} , result: {}".format(i, 100 - i, calculate_probabilities(i, 100 - i)))


# test_calculate_probabilities()

def test_update_result():
    with FootballMatchesDatabase() as db, DongqiudiCrawler() as crawler:
        game_id = "53637089"


        match_info = DbMatchInfo(db.get_match_by_id(match_id=game_id))
        if match_info is None:
            print("not find match info ", game_id)
            return

        print(match_info)
        print(type(match_info))

        g_game_detail = crawler.get_game_detail(game_id)

        header_info = GetHeaderInfo(g_game_detail)

        match_result = MatchResult(header_info)
        match_result.check_prediction(match_info)
        print("score:{}-{}, result:{}, is_win:{}, is_gaol_num:{}, is_score:{}".format( match_result.as_a, match_result.as_b,
              match_result.result, match_result.is_win, match_result.is_goal_num, match_result.is_score))


test_update_result()