from PIL import Image, ImageDraw, ImageFont


class Poster():
    def __init__(self):
        # 准备素材
        self.team1_name = "曼联g按时交付考虑"
        self.team2_name = "利物浦"
        self.match_time = "2022-01-01 14:00"
        self.match_name = "英超 第32轮"
        self.team1_icon = "1.png"
        self.team2_icon = "2.png"
        self.team1_league_info = "积分：10，排名：1，近5场：3胜2平1负，球队状况：良好"
        self.team2_league_info = "积分：8，排名：2，近5场：2胜3平1负，球队状况：一般"
        self.match_history = "近6场对战记录：Team A 4胜2负，Team B 3胜3负"
        self.background_color = (255, 255, 255)  # 背景颜色

        # 创建海报背景

        # 创建海报三部分
        # 1. 比赛标题、球队图标、基本元素
        self.game_title_background = Image.new("RGBA", (700, 250), self.background_color)
        # 2. 分析
        self.game_anlay_background = Image.new("RGBA", (700, 1180), self.background_color)
        # 3. 预测推荐
        self.game_predict_background = Image.new("RGBA", (700, 200), self.background_color)
        # 4. 公众号关注 和 免责提示
        self.notice_background = Image.new("RGBA", (700, 500), self.background_color)

        self.width = 700

        self.game_title_draw = ImageDraw.Draw(self.game_title_background)
        self.game_anlay_draw = ImageDraw.Draw(self.game_anlay_background)
        self.game_predict_draw = ImageDraw.Draw(self.game_predict_background)
        self.notice_draw = ImageDraw.Draw(self.notice_background)

    def draw_team_icon(self, team_type: str):
        # 添加球队图标

        team_icon_image = Image.open(self.team1_icon)
        if team_type == "away":
            team_icon_image = Image.open(self.team2_icon)

        # 确保两个图像具有相同的透明度通道
        if team_icon_image.mode != "RGBA":
            team_icon_image = team_icon_image.convert("RGBA")

        team_icon_image = team_icon_image.resize((150, 150))
        icon_x = (self.width // 2 - team_icon_image.width) // 2
        icon_y = (self.game_title_background.height // 2 - team_icon_image.height) // 2 + 20
        if team_type == "home":
            self.game_title_background.alpha_composite(team_icon_image, (icon_x - 50, icon_y))
        else:
            self.game_title_background.alpha_composite(team_icon_image, (icon_x + 350 + 50, icon_y))

    def draw_match_name(self):

        # 添加队名和比赛信息
        font = ImageFont.truetype("msyhbd.ttc", 45)
        # textsize 是 pillow 9.5.0 版本才有
        # textsize is deprecated and will be removed in Pillow 10 (2023-07-01). Use textbbox or textlength instead.
        text_width, text_height = self.game_title_draw.textsize(self.match_name, font=font)
        # print(text_width, text_height)

        # # 计算文本的位置
        x = (self.width - text_width) // 2
        y = (self.game_title_background.height - text_height) // 2
        #
        self.game_title_draw.text((x, 10), self.match_name, font=font, fill=(0, 0, 0))

    def draw_match_team_name(self):
        font = ImageFont.truetype("msyhbd.ttc", 40)
        # textsize 是 pillow 9.5.0 版本才有
        # textsize is deprecated and will be removed in Pillow 10 (2023-07-01). Use textbbox or textlength instead.

        match_vs_text = " VS "
        # match_team_name = self.team1_name +  + self.team2_name

        text_width, text_height = self.game_title_draw.textsize(match_vs_text, font=font)
        # print("111",text_width, text_height)

        # # 计算文本的位置
        x = (self.width - text_width) // 2
        y = (self.game_title_background.height - text_height) // 2
        #
        self.game_title_draw.text((x, 80), match_vs_text, font=font, fill=(0, 0, 0))

        # 绘制队名在图片下方
        name_font = ImageFont.truetype("msyhbd.ttc", 20)
        text_width, text_height = self.game_title_draw.textsize(self.team1_name, font=name_font)
        name_x = (self.width // 2 - text_width) // 2
        self.game_title_draw.text((name_x - 50, 200), self.team1_name, font=name_font, fill=(0, 0, 0))

        text_width, text_height = self.game_title_draw.textsize(self.team2_name, font=name_font)
        name_x = (self.width // 2 - text_width) // 2
        self.game_title_draw.text((name_x + self.width // 2 + 50, 200), self.team2_name, font=name_font, fill=(0, 0, 0))

        # x_separate_image = Image.new("RGBA", (self.width, 20), (255, 221, 102))
        # self.game_title_background.paste(x_separate_image, (0, 480), x_separate_image)

    def draw_match_time(self):
        font = ImageFont.truetype("msyhbd.ttc", 30)

        text_width, text_height = self.game_title_draw.textsize(self.match_time, font=font)
        # print(text_width, text_height)

        # # 计算文本的位置
        x = (self.width - text_width) // 2
        y = (self.game_title_background.height - text_height) // 2
        self.game_title_draw.text((x, 150), self.match_time, font=font, fill=(255, 17, 17))

    def draw_separate(self):
        # 绘制分隔符
        # 创建海报背景
        x_separate_image = Image.new("RGBA", (self.width, 20), (255, 221, 102))
        self.game_anlay_background.paste(x_separate_image, (0, 0), x_separate_image)
        self.game_anlay_background.paste(x_separate_image, (0, 680), x_separate_image)
        y_separate_image = Image.new("RGBA", (5, 660), (15, 164, 193))
        self.game_anlay_background.paste(y_separate_image, ((self.width - y_separate_image.width) // 2, 20),
                                         y_separate_image)

    def draw_long_message(self, long_text, font, begin_y, x_side, fill=(0, 0, 0)):
        def wrap_text(max_width):
            """
            根据给定的最大宽度将文本分割成多行。
            """
            lines = []
            current_line = ''
            current_width = 0

            for char in long_text:
                # 获取当前字符的宽度
                char_width, char_height = self.game_anlay_draw.textsize(char, font)

                # 检查当前行加上新字符后的宽度是否超过最大宽度
                if current_width + char_width > max_width:
                    lines.append(current_line)
                    current_line = char
                    current_width = char_width
                else:
                    current_line += char
                    current_width += char_width

                    # 不要忘记添加最后一行
            if current_line:
                lines.append(current_line)

            return lines

        max_width = 300  # 你期望的最大宽度，单位是像素

        # 分割文本
        lines = wrap_text(max_width)

        # 计算文本绘制的起始y坐标
        line_spacing = font.getsize('中')[1]  # 使用'中'字的高度作为行间距
        # 遍历分割后的每一行文本，并绘制它们
        for line in lines:
            self.game_anlay_draw.text((x_side, begin_y), line, font=font, fill=fill)
            begin_y += font.getsize(line)[1] + line_spacing  # 更新y坐标以绘制下一行

        return begin_y

    def draw_team_message(self, team_message: dict, team_type: str):
        """
        文本生成
        * 联赛情况: 排名西甲第13，10胜7平15负，积37分, 胜率32%
        * 近5场比赛：负、负、负、负、负、
        * 近5场进攻状态： 近五场，进球1，场均进球0.2。进攻低迷。
        * 近5场防守状态： 近五场，失球10，场均失球2.0，防守漏洞百出。
        * 交锋历史： 就浪费大家利夫卡是的克里夫剧场那边现在处女星座快女
        * 球员情况： ysdjflkashdfglhaslgjaslkjfkladsjfdsaldsasd.
        * 球队情况： 家里的撒房间阿里山扩大飞机率你们在内心 加大放假啦v在线就打算飞机场v下 饭卡看到郡县制v努力形成子女的萨芬萨聚氯女性创作，vn角度考虑封禁查询中家里的撒房间阿里山扩大飞机率你们在内心 加大放假啦v在线就打算飞机场v下

        :return:
        """
        name_font = ImageFont.truetype("msyh.ttc", 25)
        name_text = team_message["name"]
        name_color = (0, 0, 0)
        if team_type == "home":
            name_color = (13, 102, 171)
        else:
            name_color = (241, 141, 65)
        font = ImageFont.truetype("msyh.ttc", 20)  # 微软雅黑 20号字体
        league_text = team_message["league_text"]
        recent_match_text = team_message["recent_match_text"]
        recent_comp_text = team_message["recent_comp_text"]
        crew_status_text = team_message["crew_status_text"]
        team_status_text = team_message["team_status_text"]
        x_side = 10  # 侧边间隔
        if team_type == "home":
            x_side = 15  # 侧边间隔
        else:
            x_side = 365
        y_side = 10  # 上边间隔
        begin_y = 40
        begin_y = self.draw_long_message(name_text, name_font, begin_y, x_side + 20, name_color) + y_side
        begin_y = self.draw_long_message(league_text, font, begin_y, x_side) + y_side
        begin_y = self.draw_long_message(recent_match_text, font, begin_y, x_side) + y_side
        begin_y = self.draw_long_message(recent_comp_text, font, begin_y, x_side) + y_side
        begin_y = self.draw_long_message(crew_status_text, font, begin_y, x_side) + y_side
        # begin_y = self.draw_long_message(team_status_text, font, begin_y, x_side) + y_side

    def draw_algorithm_predict(self, pre_info: dict):
        """
        :return:
        """
        title_font = ImageFont.truetype("msyhbd.ttc", 35)
        content_font = ImageFont.truetype("msyh.ttc", 30)  # 微软雅黑 20号字体
        predict_title_text = "【大数据预测】"
        predict_index_text = "推荐指数:\n胜:{}%,平:{}%,负:{}%".format(pre_info["win_advice_index"],
                                                                      pre_info["draw_advice_index"],
                                                                      pre_info["loss_advice_index"])
        team_predict_text = "主队胜指数：{}, 客队胜指数 {}".format(pre_info["home_win_index"],
                                                                  pre_info["away_win_index"])
        home_team_text = "主队进球指数: {}, 失球指数: {}".format(pre_info["home_attack_index"],
                                                                 pre_info["home_lose_index"])
        away_team_text = "客队进球指数 {}, 失球指数 {}".format(pre_info["away_attack_index"],
                                                               pre_info["away_lose_index"])
        predict_goal_number_text = "预测进球数 {}".format(pre_info["all_goal_index"])
        predict_goal_text = "比分预测：{}-{}".format(pre_info["home_goal"], pre_info["away_goal"])

        x_side = 50  # 侧边间隔

        y_side = 50  # 上边间隔
        begin_y = 730

        self.game_anlay_draw.text((x_side, begin_y), text=predict_title_text, font=title_font, fill=(0, 0, 0))
        begin_y = begin_y + 60
        x_side = 120
        self.game_anlay_draw.text((80, begin_y), text=predict_index_text, font=title_font, fill=(255, 0, 0))
        begin_y = begin_y + y_side + 40
        self.game_anlay_draw.text((x_side, begin_y), text=team_predict_text, font=content_font, fill=(0, 0, 0))
        begin_y = begin_y + y_side
        self.game_anlay_draw.text((x_side, begin_y), text=home_team_text, font=content_font, fill=(0, 0, 0))
        begin_y = begin_y + y_side
        self.game_anlay_draw.text((x_side, begin_y), text=away_team_text, font=content_font, fill=(0, 0, 0))
        begin_y = begin_y + y_side
        self.game_anlay_draw.text((x_side, begin_y), text=predict_goal_number_text, font=content_font, fill=(0, 0, 0))
        begin_y = begin_y + y_side
        self.game_anlay_draw.text((x_side, begin_y), text=predict_goal_text, font=content_font, fill=(0, 0, 0))

    def draw_author_predict(self, author_info: dict):
        title_font = ImageFont.truetype("msyhbd.ttc", 35)
        content_font = ImageFont.truetype("msyh.ttc", 30)  # 微软雅黑 20号字体
        author_title_text = "【笔者推荐】"
        win_text = self.team1_name + " " + author_info["win_text"]
        goal_number_text = "进球数{}".format(author_info["goal_number_text"])
        goal_text = "比分{}".format(author_info["goal_text"])
        x_side = 50  # 侧边间隔
        y_side = 40  # 上边间隔
        begin_y = 5
        self.game_predict_draw.text((x_side, begin_y), text=author_title_text, font=title_font, fill=(0, 0, 0))
        begin_y = begin_y + 60
        x_side = 120
        self.game_predict_draw.text((x_side, begin_y), text=win_text, font=content_font, fill=(255, 0, 0))
        begin_y = begin_y + y_side
        self.game_predict_draw.text((x_side, begin_y), text=goal_number_text, font=content_font, fill=(255, 0, 0))
        begin_y = begin_y + y_side
        self.game_predict_draw.text((x_side, begin_y), text=goal_text, font=content_font, fill=(255, 0, 0))
        begin_y = begin_y + y_side

    def show(self, com_info, pre_info, author_info):
        self.draw_team_icon("home")  # 绘制主队图标
        self.draw_team_icon("away")  # 绘制客队图标
        self.draw_match_name()  # 绘制比赛名称
        self.draw_match_team_name()  # 绘制 主队名称V客队名称
        self.draw_match_time()  # 绘制 比赛时间
        self.draw_separate()  # 绘制 分隔符
        self.draw_team_message(com_info["home_team"], "home")  # 绘制球队信息
        self.draw_team_message(com_info["away_team"], "away")  # 绘制球队信息
        self.draw_algorithm_predict(pre_info)
        self.draw_author_predict(author_info)
        # self.game_title_background.save("1111.png")
        # self.game_anlay_background.save("2222.png")
        # self.game_predict_background.save("3333.png")

        # 计算新图片的高度（两张图片的高度之和）
        new_height = self.game_title_background.height + self.game_anlay_background.height + self.game_predict_background.height
        # 宽度保持不变（取第一张图片的宽度）
        new_width = self.game_title_background.width

        # 创建一个新的空白图片，大小为(new_width, new_height)
        new_img = Image.new('RGB', (new_width, new_height))
        # 将两张图片粘贴到新图片上
        new_img.paste(self.game_title_background, (0, 0))  # 粘贴第一张图片到(0, 0)位置
        new_img.paste(self.game_anlay_background, (0, self.game_title_background.height))  # 粘贴第二张图片到(0, img1.height)位置
        new_img.paste(self.game_predict_background,
                      (0, self.game_title_background.height + self.game_anlay_background.height))
        # 保存新图片
        new_img.save('0000.png')
        new_img.show()
        # self.game_anlay_background.show()
        # self.game_predict_background.show()

    def show_without_author(self,com_info, pre_info):
        self.draw_team_icon("home")  # 绘制主队图标
        self.draw_team_icon("away")  # 绘制客队图标
        self.draw_match_name()  # 绘制比赛名称
        self.draw_match_team_name()  # 绘制 主队名称V客队名称
        self.draw_match_time()  # 绘制 比赛时间
        self.draw_separate()  # 绘制 分隔符
        home_team = com_info["home_team"]
        away_team = com_info["away_team"]
        self.draw_team_message(home_team, "home")  # 绘制球队信息
        self.draw_team_message(away_team, "away")  # 绘制球队信息
        self.draw_algorithm_predict(pre_info)

        # 计算新图片的高度（两张图片的高度之和）
        new_height = self.game_title_background.height + self.game_anlay_background.height
        # 宽度保持不变（取第一张图片的宽度）
        new_width = self.game_title_background.width

        # 创建一个新的空白图片，大小为(new_width, new_height)
        new_img = Image.new('RGB', (new_width, new_height))
        # 将两张图片粘贴到新图片上
        new_img.paste(self.game_title_background, (0, 0))  # 粘贴第一张图片到(0, 0)位置
        new_img.paste(self.game_anlay_background, (0, self.game_title_background.height))  # 粘贴第二张图片到(0, img1.height)位置


        file_name = home_team["name"]+"vs"+away_team["name"]+".png"
        path = "./src/ai_picture/"+file_name
        # 保存新图片
        print("save path:",path)
        new_img.save(path)