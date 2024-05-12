import json
from selenium import webdriver
import time
import util


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

    # 使用上下文管理协议（with 语句）来确保资源正确释放

#
# with DongqiudiCrawler() as crawler:
#     # all_info = crawler.get_games_all_info(1)
#     # 可以继续调用其他方法，如 get_game_detail
#     # game_detail = crawler.get_game_detail('some_game_id')
#     crawler.get_game_detail("53637089")
# # 浏览器实例在 with 语句块结束后自动关闭
