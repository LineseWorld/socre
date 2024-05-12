from selenium import webdriver
import time
import json
import util

# 废弃
def GetGamesAllInfo(index: int):
    """
    :param index: 1 是英超
    :return:
    """
    # 创建一个Chrome浏览器实例
    driver = webdriver.Chrome()
    # 打开目标网页
    url = 'https://www.dongqiudi.com/data' + '/1'
    driver.get(url)
    # 等待JavaScript加载完成
    time.sleep(5)
    # 获取window.__NUXT__数据内容
    nust_data = driver.execute_script("return window.__NUXT__;")
    # 打印结果
    new_data = str(nust_data)
    new_data = new_data.replace("'", "\"")
    new_data = new_data.replace(": None", ": null")
    new_data = new_data.replace(": False", ": false")
    new_data = new_data.replace(": True", ": true")
    json_data = json.loads(new_data)
    # 关闭浏览器实例
    driver.quit()
    return json_data

# 实现单次比赛信息获取
def GetGameDetail(game_id: str):
    # 创建一个Chrome浏览器实例
    print("GetGameDetail Chrome begin")
    driver = webdriver.Chrome()
    # 打开目标网页
    url = 'https://www.dongqiudi.com/liveDetail/' + game_id
    driver.get(url)
    print("GetGameDetail get url end")
    # 等待JavaScript加载完成
    time.sleep(5)
    # 获取window.__NUXT__数据内容
    nust_data = driver.execute_script("return window.__NUXT__;")
    new_data = str(nust_data)
    new_data = util.ToJsonString(new_data)
    json_data = json.loads(new_data)
    # 关闭浏览器实例
    driver.quit()
    return json_data


def GetHeaderInfo(json_data: dict):
    data = json_data["data"]
    data = data[0]
    return data["headerInfo"]


def GetAnalysisInitData(json_data: dict):
    data = json_data["data"]
    data = data[0]
    return data["analysisInitData"]
