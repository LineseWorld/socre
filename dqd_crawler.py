import json
from selenium import webdriver
import time
import util
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def GetHeaderInfo(json_data: dict):
    data = json_data["data"]
    data = data[0]
    return data["headerInfo"]


def GetAnalysisInitData(json_data: dict):
    data = json_data["data"]
    data = data[0]
    return data["analysisInitData"]


class DongqiudiCrawler:
    def __init__(self):
        self.driver = webdriver.Chrome()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()

    def get_games_all_info(self, index: str):
        url = f'https://www.dongqiudi.com/data/{index}'
        self.driver.get(url)

        # 使用 WebDriverWait 等待特定的条件，比如某个元素出现
        # 这里假设有一个特定的元素可以表明页面已加载完成，例如 ID 为 "content-loaded" 的元素
        # try:
        #     WebDriverWait(self.driver, 10).until(
        #         EC.presence_of_element_located((By.ID, "content-loaded"))
        #     )
        # except Exception as e:
        #     print(f"等待元素失败: {e}")

        # 获取 window.__NUXT__ 数据内容
        nust_data = self.driver.execute_script("return window.__NUXT__;")
        cleaned_data = self._clean_nust_data(nust_data)
        json_data = json.loads(cleaned_data)
        return json_data

    def get_game_detail(self, game_id: str):
        url = f'https://www.dongqiudi.com/liveDetail/{game_id}'
        self.driver.get(url)

        time.sleep(5)
        # 同样使用 WebDriverWait 等待特定的条件
        # try:
        #     WebDriverWait(self.driver, 10).until(
        #         EC.presence_of_element_located((By.ID, "game-detail-loaded"))
        #     )
        # except Exception as e:
        #     print(f"等待元素失败: {e}")

        # 获取 window.__NUXT__ 数据内容
        nust_data = self.driver.execute_script("return window.__NUXT__;")
        new_data = str(nust_data)
        new_data = util.ToJsonString(new_data)
        json_data = json.loads(new_data)
        return json_data

    def _clean_nust_data(self, nust_data):
        # 清理数据的函数
        new_data = str(nust_data)
        new_data = new_data.replace("'", "\"")
        new_data = new_data.replace(": None", ": null")
        new_data = new_data.replace(": False", ": false")
        new_data = new_data.replace(": True", ": true")
        return new_data

    def get_match_list_from_lottery(self):
        url = "https://www.lottery.gov.cn/jc/index.html"
        # 访问网页
        self.driver.get(url)

        # 等待动态内容加载完成（例如，等待某个元素出现）
        wait = WebDriverWait(self.driver, 10)
        element = wait.until(EC.visibility_of_element_located((By.ID, "zqszData")))

        # 查找table元素（如果它位于element内部）
        # 注意：如果table元素是element的直接子元素，这种方法有效
        # 如果不是，你可能需要递归搜索或调整定位器
        table = element.find_element(By.TAG_NAME, 'table')

        # 提取表格中的数据
        rows = table.find_elements(By.TAG_NAME, 'tr')

        result = dict()

        one_day_match_list = []
        day_key = ""
        day_count = 0
        for row in rows:
            # 提取周赛事
            headers = row.find_elements(By.CSS_SELECTOR, 'th.dateRace.text-left.p-l3')

            if headers:
                for header in headers:
                    if day_count != 0:
                        result[day_key] = one_day_match_list
                    day_key = header.text
                    day_count += 1
                    one_day_match_list = []
                    print(header.text)

            cells = row.find_elements(By.TAG_NAME, 'td')  # 或使用'th'取决于表格结构
            cell_texts = [cell.text for cell in cells]
            one_match = dict()
            if len(cell_texts) > 0:
                one_match["number"] = cell_texts[0]
                one_match["match_name"] = cell_texts[1]
                one_match["team_vs_team"] = cell_texts[2]
                one_match["match_time"] = cell_texts[3]

                one_day_match_list.append(one_match)

            print(cell_texts)

        if day_count != 0:
            result[day_key] = one_day_match_list

        print(result)
        return result
