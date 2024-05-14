# 实现输入参数，生成球队模板

import config
from football_team import FootballTeam
from competition import Competition
from battle import Battle
from prediction import Prediction
from draw3 import Poster
import download
from football_matches_database import FootballMatchesDatabase, DbMatchInfo
import json
from datetime import datetime
from dqd_crawler import *
from match_result import MatchResult


def update_played_game(db: FootballMatchesDatabase, crawler: DongqiudiCrawler):
    # 更新已经完成比赛的数据
    print("正在更新过往比赛...")
    matchs = db.query_not_result_matches()
    all_update_count = 0
    right_count = 0
    right_win_count = 0
    right_goal_num_count = 0
    right_score_count = 0
    current_timestamp = time.time()  # 当前时间戳 单位 秒
    for match in matchs:
        match_info = DbMatchInfo(match)
        print("====matchId：{}====".format(match_info.match_id))
        print("记录比赛结果中 {} {} vs {} 比赛时间{} ...".format(match_info.match_title, match_info.team_a_name,
                                                                 match_info.team_b_name, match_info.match_time))

        if current_timestamp <= match_info.match_time_stamp + 120 * 60:
            # 当前时间 和比赛开始时间相比，差120分钟 就认为比赛还没结束
            print("===比赛还没开始 或者 还没有结束，下一个比赛====")
            continue

        json_data = crawler.get_game_detail(match_info.match_id)
        header_info = GetHeaderInfo(json_data)

        match_result = MatchResult(header_info)

        if match_result.status != "Played":
            print("===比赛还没开始 或者 还没有结束，下一个比赛====")
            continue

        match_result.check_prediction(match_info)

        print("结果比分:{}-{}, 胜负预测:{}，进球数预测{}，比分预测{}".format(
            match_result.as_a,
            match_result.as_b,
            match_info.author_predict_win,
            match_info.author_predict_goal_num,
            match_info.author_predict_score))
        print("胜负命中:{}, 进球数命中:{}, 比分命中:{}".format(
            match_result.is_win,
            match_result.is_goal_num,
            match_result.is_score))

        update_data = {
            'match_id': match_info.match_id,
            'result': "{}-{}".format(match_result.as_a,
                                     match_result.as_b),
            'is_right_win': match_result.is_win,
            'is_right_goal_num': match_result.is_goal_num,
            'is_right_score': match_result.is_score,
        }
        db.insert_or_update_match(update_data)
        all_update_count += 1

        if match_result.is_win:
            right_win_count += 1
        if match_result.is_goal_num:
            right_goal_num_count += 1
        if match_result.is_score:
            right_score_count += 1

        if match_result.is_win or match_result.is_goal_num or match_result.is_score:
            right_count += 1
        print("======更新======")
    print("完成更新，更新汇总如下")

    print("总共更新{}场，总体命中{}场，胜负命中{}，进球数命中：{}，比分命中：{}".format(all_update_count, right_count,
                                                                                  right_win_count, right_goal_num_count,
                                                                                  right_score_count))

    if all_update_count != 0:
        print("总命中率：%.2f，胜负命中率：%.2f，进球数命中率：%.2f，比分命中率：%.2f" % (
            right_count / all_update_count, right_win_count / all_update_count, right_goal_num_count / all_update_count,
            right_score_count / all_update_count))


def generate_game_match(db: FootballMatchesDatabase, crawler: DongqiudiCrawler):

    while True:
        match_id = input("输入比赛id：")
        if match_id == "end":
            break
        g_game_detail = crawler.get_game_detail(match_id)

        # print(type(g_game_detail))
        header_info = GetHeaderInfo(g_game_detail)

        analysis_init_data = GetAnalysisInitData(g_game_detail)

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

        # 插入数据
        # 字符串日期时间
        date_string = com_info["match_time"]

        # 将字符串转换为datetime对象
        dt_object = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')

        # 将datetime对象转换为时间戳
        timestamp = dt_object.timestamp()
        match_data = {
            'match_id': match_id,
            'match_time': com_info["match_time"],
            'match_time_stamp': timestamp,
            'match_title': com_info["match_name"],
            'team_a_name': home_team["name"],
            'team_b_name': away_team["name"],
            'team_a_info': json.dumps(home_team, ensure_ascii=False),
            'team_b_info': json.dumps(away_team, ensure_ascii=False),
            'ai_predict_info': json.dumps(pre_info),
            'author_predict_win': author_win,
            'author_predict_goal_num': author_goal,
            'author_predict_score': author_score,
        }
        db.insert_or_replace_match(match_data)
        print("insert db success, data:[{}]".format(match_data))

        p.show(com_info, pre_info, author_info)


def get_ai_predict_list(crawler: DongqiudiCrawler):
    """
    根据将lottery的数据 生成每一张图片
    :return:
    """
    lottery_dict = crawler.get_match_list_from_lottery()
    for day, day_matches in lottery_dict.items():
        print(f"--- {day} 的赛事 ---")
        for match in day_matches:
            number = match['number']
            match_name = match['match_name']
            team_vs_team = match['team_vs_team']
            match_time = match['match_time']
            print(f"赛事编号: {number}, 赛事名称: {match_name}, 对阵双方: {team_vs_team}, 比赛时间: {match_time}")
        print()  # 在每个日期的比赛之后加一个空行，以便分隔


if __name__ == '__main__':
    with FootballMatchesDatabase() as db, DongqiudiCrawler() as crawler:
        get_ai_predict_list(crawler)

        # 更新过往比赛才开启
        # update_played_game(db, crawler)


        # generate_game_match(db, crawler)
