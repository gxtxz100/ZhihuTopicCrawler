# Get all questions from topics

# Input: Topic ID
# Output: A list of questions with other meta-data: Question ID, Question Text, Question Data, Question URL
# Last Run: 2024/11/16 12:32


import os
import json
import pandas as pd
from datetime import datetime
from get_url_text import get_url_text

def parseJson(text):
    json_data = json.loads(text)
    lst = json_data["data"]
    nextUrl = json_data["paging"]["next"]

    if not lst:
        return

    for item in lst:
        type = item["target"]["type"]

        if type == "answer":
            # Answer 回答
            cn_type = "问题_来自回答"
            question = item["target"]["question"]
            id = question["id"]
            title = question["title"]
            url = "https://www.zhihu.com/question/" + str(id)
            question_date = datetime.fromtimestamp(question["created"]).strftime(
                "%Y-%m-%d"
            )
            # question_follower = question['follower_count']
            # answer_count = question['answer_count']
            # print("问题：", id, title)
            sml_list = [cn_type, id, title, url, question_date]
            q_list.append(sml_list)

        elif type == "question":
            # Question 问题
            cn_type = "问题"
            question = item["target"]
            id = question["id"]
            title = question["title"]
            url = "https://www.zhihu.com/question/" + str(id)
            question_date = datetime.fromtimestamp(question["created"]).strftime(
                "%Y-%m-%d"
            )
            # question_follower = question['follower_count']
            # answer_count = question['answer_count']
            # print("问题：", id, title)
            sml_list = [cn_type, id, title, url, question_date]
            q_list.append(sml_list)

        elif type == "article":
            # Article 专栏
            cn_type = "专栏"
            zhuanlan = item["target"]
            id = zhuanlan["id"]
            title = zhuanlan["title"]
            url = zhuanlan["url"]
            article_date = datetime.fromtimestamp(zhuanlan["created"]).strftime(
                "%Y-%m-%d"
            )
            # vote = zhuanlan['voteup_count']
            # cmts = zhuanlan['comment_count']
            # auth = zhuanlan['author']['name']
            # print("专栏：", id, title)
            sml_list = [cn_type, id, title, url, article_date]
            q_list.append(sml_list)

    return nextUrl

def save_data(q_list, filename):

    df = pd.DataFrame(q_list, columns=["type", "id", "title", "url", "date"])
    # 根据id去重，并按照时间排序
    df = df.drop_duplicates(subset=["id"]).sort_values(by="date")

    # 若文件已存在，则读取原文件，合并后去重，实现文件更新

    if os.path.exists(filename):
        df_original = pd.read_csv(filename)
        df = pd.concat([df_original, df], ignore_index=True)
        df = df.drop_duplicates(subset=["id"]).sort_values(by="date")

    df.to_csv(filename, index=False, header=True, encoding="utf-8")

    print(f"共保存{len(df)}条数据到{filename}")

def crawl_1(topicID):
    # Discussion 讨论
    url = (
        "https://www.zhihu.com/api/v5.1/topics/"
        + topicID
        + "/feeds/essence/v2?offset=0&limit=50"
    )
    while url:
        try:
            text = get_url_text(url)
            url = parseJson(text)
        except:
            print(f"目前已有{len(q_list)}条数据")
            break

    url = (
        "https://www.zhihu.com/api/v5.1/topics/"
        + topicID
        + "/feeds/timeline_activity/v2?offset=0&limit=50"
    )
    while url:
        try:
            text = get_url_text(url)
            url = parseJson(text)
        except:
            print(f"目前已有{len(q_list)}条数据")
            break

    print("crawl_讨论: 完成")

def crawl_2(topicID):
    # Selected posts 精华
    url = (
        "https://www.zhihu.com/api/v5.1/topics/"
        + topicID
        + "/feeds/top_activity/v2?offset=0&limit=50"
    )
    while url:
        try:
            text = get_url_text(url)
            url = parseJson(text)
        except:
            print(f"目前已有{len(q_list)}条数据")
            break
    print("crawl_精华: 完成")

def crawl_3(topicID):
    # Awaiting answers 等待回答
    url = (
        "https://www.zhihu.com/api/v5.1/topics/"
        + topicID
        + "/feeds/top_question/v2?offset=0&limit=50"
    )
    while url:
        try:
            text = get_url_text(url)
            url = parseJson(text)
        except:
            print(f"目前已有{len(q_list)}条数据")
            break

    url = (
        "https://www.zhihu.com/api/v5.1/topics/"
        + topicID
        + "/feeds/new_question/v2?offset=0&limit=50"
    )
    while url:
        try:
            text = get_url_text(url)
            url = parseJson(text)
        except:
            print(f"目前已有{len(q_list)}条数据")
            break

    print("crawl_等待回答: 完成")

if __name__ == "__main__":
    # 漩涡鸣人: 20204759
    # 春野樱: 20135411
    #TODO 指定要爬取的话题ID
    topicID_list = ["20204759", "20135411"]
    q_list = []

    for topicID in topicID_list:
        crawl_1(topicID)
        crawl_2(topicID)
        crawl_3(topicID)
        save_data(q_list, "data/question_list.csv")
