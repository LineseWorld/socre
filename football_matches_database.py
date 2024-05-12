import sqlite3
import datetime
from sqlite3 import Error


class FootballMatchesDatabase:
    def __init__(self, db_name='football_matches.db'):
        self.db_name = db_name
        self.conn = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def close(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def create_table(self):
        create_table_sql = '''  
        CREATE TABLE IF NOT EXISTS football_matches (  
            match_id TEXT PRIMARY KEY,  
            match_time TEXT,  
            match_time_stamp INTEGER,  
            match_title TEXT,  
            team_a_name TEXT,  
            team_b_name TEXT,  
            team_a_info TEXT,  
            team_b_info TEXT,  
            ai_predict_info TEXT,  
            author_predict_win TEXT,  
            author_predict_goal_num TEXT,  
            author_predict_score TEXT,  
            result TEXT,  
            is_right_win BOOLEAN,  
            is_right_goal_num BOOLEAN,  
            is_right_score BOOLEAN  
        );  
        '''
        self.cursor.execute(create_table_sql)
        self.conn.commit()

    def insert_or_replace_match(self, match_data):
        # 假设match_data包含了一个名为'match_id'的键，它作为主键
        # 并且其他键对应于表中的列
        columns = ', '.join(match_data.keys())
        placeholders = ', '.join(['?'] * len(match_data))

        # 使用INSERT OR REPLACE语句
        sql = f'''  
        INSERT OR REPLACE INTO football_matches ({columns})  
        VALUES ({placeholders});  
        '''
        try:
            # 传递所有值的列表作为参数
            params = list(match_data.values())
            self.cursor.execute(sql, params)
            self.conn.commit()
        except Error as e:
            print(f"An error occurred: {e.args[0]}")

    def insert_or_update_match(self, match_data):
        # 假设match_data包含了一个名为'match_id'的键，它作为主键
        # 并且其他键对应于表中的列，但我们只更新其中的一些

        # 构造要更新的字段和值
        update_fields = []
        update_placeholders = []
        for key, value in match_data.items():
            if key != 'match_id':  # 跳过主键，因为它用于WHERE子句
                update_fields.append(f"{key}=?")
                update_placeholders.append(value)

                # 使用UPDATE语句
        sql = f'''  
        UPDATE football_matches  
        SET {', '.join(update_fields)}  
        WHERE match_id=?;  
        '''

        # 添加主键到参数列表的末尾
        update_placeholders.append(match_data['match_id'])

        try:
            # 传递所有值的列表作为参数
            self.cursor.execute(sql, update_placeholders)
            self.conn.commit()
        except Error as e:
            print(f"An error occurred: {e.args[0]}")

    def query_all_matches(self):
        query_all_sql = 'SELECT * FROM football_matches;'
        self.cursor.execute(query_all_sql)
        rows = self.cursor.fetchall()
        return rows

    def get_match_by_id(self, match_id):
        # 假设football_matches表中有一个名为match_id的列
        sql = "SELECT * FROM football_matches WHERE match_id=?"

        try:
            self.cursor.execute(sql, (match_id,))
            result = self.cursor.fetchone()
            if result:
                return result
            else:
                return None
        except Error as e:
            print(f"An error occurred: {e.args[0]}")
            return None

    def delete_match(self, match_id):
        delete_sql = 'DELETE FROM football_matches WHERE match_id = ?;'
        self.cursor.execute(delete_sql, (match_id,))
        self.conn.commit()

    def query_not_result_matches(self):
        query_all_sql = 'SELECT * FROM football_matches WHERE result IS NULL;'
        self.cursor.execute(query_all_sql)
        rows = self.cursor.fetchall()
        return rows


# if __name__ == "__main__":
#     with FootballMatchesDatabase() as db:
#         # 插入数据
#         match_data = {
#             'match_id': 1,
#             'match_title': 'asdfasdfas'
#         }
#         db.insert_or_replace_match(match_data)


class DbMatchInfo():
    def __init__(self, db_result):
        # print(db_result)
        self.match_id = db_result[0]
        self.match_time = db_result[1]
        self.match_time_stamp = db_result[2]
        self.match_title = db_result[3]
        self.team_a_name = db_result[4]
        self.team_b_name = db_result[5]
        self.team_a_info = db_result[6]
        self.team_b_info = db_result[7]
        self.ai_predict_info = db_result[8]
        self.author_predict_win = db_result[9]
        self.author_predict_goal_num = db_result[10]
        self.author_predict_score = db_result[11]
        self.result = db_result[12]
        self.is_right_win = db_result[13]
        self.is_right_goal_num = db_result[14]
        self.is_right_score = db_result[15]
