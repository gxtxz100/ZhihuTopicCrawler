# Get answer posts and answer post meta-data by question ID

# Last Run: 2024/11/16 12:55
# About this script:
# **Input**: A list of question ID
# **Output**: A list of answer posts and answer post meta-data by question ID: Answer post text, answer date, upvote count, comment count, answer ID, author name, author gender, author follower count, author bio, author username
# Last Run: 2025/1/9 1:38

import re
import os
import json
import time
import pandas as pd
from datetime import datetime
from get_url_text import get_url_text

def get_q_list(filename):
    df = pd.read_csv(filename, encoding="utf-8")
    df = df[df["answerCount"] > 5]  # 默认爬取回答数大于5的问题
    df = df[df["created_date"] >= "2024-10-15"]  # 可选要更新的问题的时间范围
    
    questions_dict = dict(zip(df["q_id"].tolist(), df["q_content"].tolist()))
    
    print(f"共有 {len(questions_dict)} 个回答数大于5且不重复的问题")

    return dict(reversed(questions_dict.items()))   # 从后往前爬

def parse_data(url, q_id):
    text = get_url_text(url)
    
    try:
        json_data = json.loads(text)["data"]
        next_url = json.loads(text)["paging"]["next"]
        is_end = json.loads(text)["paging"]["is_end"]
    except Exception as e:
        print(f"Error: {url}")
        print(e)

    one_q_all_answer = []

    for item in json_data:
        one_answer_list = []

        question_id = q_id  # Question id
        answer_content = item["target"]["content"]
        answer_content = re.sub("<[^<]+?>", "", answer_content)
        answer_date = datetime.fromtimestamp(item["target"]["created_time"]).strftime(
            "%Y-%m-%d"
        )  # Answer date
        answer_upvote = item["target"]["voteup_count"]  # upvote count
        answer_comment = item["target"]["comment_count"]  # comment count
        answer_id = item["target"]["id"]  # answer ID
        author_name = item["target"]["author"]["name"]  # author name
        author_gender = item["target"]["author"][
            "gender"
        ]  # author gender, 1 male 2 female
        author_url_token = item["target"]["author"]["url_token"]  # author ID
        author_follower_count = item["target"]["author"][
            "follower_count"
        ]  # author follower count
        author_headline = item["target"]["author"]["headline"]  # author bio

        one_answer_list = [
            question_id,
            answer_content,
            answer_date,
            answer_upvote,
            answer_comment,
            answer_id,
            author_name,
            author_gender,
            author_url_token,
            author_follower_count,
            author_headline,
        ]
        one_q_all_answer.append(one_answer_list)

    return one_q_all_answer, next_url, is_end
    

def save_data(answer_info, q_id):

    filename = f"data/answers_of_question/question_{str(q_id)}.csv"

    df = pd.DataFrame(
        answer_info,
        columns=[
            "q_id",
            "a_content",
            "a_date",
            "a_upvote",
            "a_comment",
            "a_id",
            "au_name",
            "au_gender",
            "au_urltoken",
            "au_followerCount",
            "au_headline",
        ],
    )
    if os.path.exists(filename):
        df_original = pd.read_csv(filename)
        df = pd.concat([df_original, df], ignore_index=True)
        df = df.drop_duplicates(subset=["a_id"]).sort_values(by="a_date")

    df.to_csv(filename, index=False, header=True)

if __name__ == "__main__":
    # TODO: 指定问题列表
    questions_dict = get_q_list("data/question_meta_info.csv")
    q_id_list = list(questions_dict.keys())
    # 也可手动输入问题 ID 以获取回答数据
    # q_list = ["24324127", "24399025"]

    # 爬一段时间会触发京东的验证码机制导致HTTPError报错，需要手动重新设置开始位置
    begin_index = 0  # 将发生报错的问题序号更新到这里即可
    for i, q_id in enumerate(q_id_list[begin_index:]):
        q_content = questions_dict.get(q_id, "None")

        print(f"\nquestion {i+begin_index} {q_content} Begin, qid: {q_id}")

        url = f"https://www.zhihu.com/api/v4/questions/{str(q_id)}/feeds?include=content%2Cauthor.follower_count"

        if_question_exist = os.path.exists(f"data/answers_of_question/question_{str(q_id)}.csv")
        get_data_by_time = False # 爬虫中是否按时间排序

        # ⚠️⚠️⚠️若按时间排序更新数据中发生报错，则需要删除该问题的对应的CSV文件，重新爬取⚠️⚠️

        if if_question_exist:
            data_existing = pd.read_csv(f"data/answers_of_question/question_{str(q_id)}.csv")
            a_id_existing = data_existing["a_id"].values.tolist()

            try:
                # 已有数据的旧问题尝试按时间排序，节省时间
                data, url, is_end = parse_data(url + "&order=updated", q_id)
                url = url + "&order=updated"
                get_data_by_time = True
            except:
                # 若不能按时间排序，则按默认顺序
                pass

        # 对于回答数很多的问题，报错时可在此处添加中途url，方便断点续爬
        # url = "" # 放入报错前最后输出的url
        # TODO

        page = 0
        is_end = False
        while not is_end:
            data, url, is_end = parse_data(url, q_id)

            save_data(data, q_id)

            if get_data_by_time:
                # 按时间排序时，若所有数据都已爬取，跳出循环，更新完成
                a_id = [item[5] for item in data]
                if all(item in a_id_existing for item in a_id):
                    break

            page += 1
            if page % 10 == 0:
                time.sleep(0.5)
                try:
                    print(url)
                    print(f"文本示例：{data[-1][1][:15]}")
                except:
                    pass

        print(f"\nquestion {i+begin_index} {q_content} Finish")

    print("Finish!!")
